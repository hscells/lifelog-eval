package com.hscells.lifelogeval.service;

import com.hscells.lifelogeval.config.ElasticSearchConfiguration;
import com.hscells.lifelogeval.model.LifelogDocument;
import org.elasticsearch.action.admin.indices.delete.DeleteIndexRequest;
import org.elasticsearch.action.admin.indices.delete.DeleteIndexResponse;
import org.elasticsearch.action.admin.indices.exists.indices.IndicesExistsRequest;
import org.elasticsearch.action.admin.indices.flush.FlushRequest;
import org.elasticsearch.action.admin.indices.get.GetIndexRequest;
import org.elasticsearch.action.delete.DeleteAction;
import org.elasticsearch.action.delete.DeleteRequest;
import org.elasticsearch.action.delete.DeleteResponse;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchRequestBuilder;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.SearchHit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

/**
 * Created by Harry Scells on 2/08/2016.
 */
public class ElasticSearchService implements AutoCloseable {

    private ElasticSearchConfiguration config;
    private Client client;

    private static final String LIFELOG_ANNOTATION_TYPE = "annotation";

    private static final Logger logger = LoggerFactory.getLogger(ElasticSearchService.class);

    public ElasticSearchService(ElasticSearchConfiguration config) throws UnknownHostException {
        this.config = config;
        Settings settings =  Settings.settingsBuilder()
                .put("cluster.name", config.getCluster())
                .build();
        client = TransportClient.builder()
                .settings(settings)
                .build()
                .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName(config.getUrl()), 9300));
    }

    private Map<String, Object> transformDocument(LifelogDocument lifelogDocument) {
        Map<String, Object> document = new HashMap<String, Object>();
        document.put("id", lifelogDocument.getId());
        for (String key : lifelogDocument.getAnnotations().keySet()) {
            document.put(key, lifelogDocument.getAnnotations().get(key));
        }
        return document;
    }

    /**
     * Add a lifelog image annotation to the index
     * @param lifelogDocument
     * @return The response from elasticsearch
     */
    public IndexResponse indexDocument(LifelogDocument lifelogDocument) {
        Map<String, Object> document = transformDocument(lifelogDocument);
        return client.prepareIndex(config.getIndex(), LIFELOG_ANNOTATION_TYPE, lifelogDocument.getId())
                .setSource(document)
                .setContentType(XContentType.JSON)
                .get();
    }

    /**
     * Add multiple lifelog image annotations to the index
     * @param lifelogDocuments
     */
    public void indexDocuments(List<LifelogDocument> lifelogDocuments) {
        for (LifelogDocument lifelogDocument : lifelogDocuments) {
            IndexResponse response = indexDocument(lifelogDocument);
            if (!response.isCreated()) {
                logger.error(String.format("Could not index document with id: %s", lifelogDocument.getId()));
            }
        }
    }

    /**
     * Delete everything, including the index
     * @return
     */
    public boolean deleteIndex() throws ExecutionException, InterruptedException {
        if (client.admin().indices().exists(new IndicesExistsRequest(config.getIndex())).get().isExists()) {
            DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest(config.getIndex());
            client.admin().indices().flush(new FlushRequest(config.getIndex())).get();
            return client.admin().indices().delete(deleteIndexRequest).get().isAcknowledged();
        }
        return true;
    }

    /**
     * Get a specific document from the index by its id
     * @param id
     * @return The response from elasticsearch
     */
    public GetResponse getDocument(String id) {
        return client.prepareGet(config.getIndex(), LIFELOG_ANNOTATION_TYPE, id).get();
    }

    /**
     * Submit a standard elasticsearch query
     * @param query A JSON string in the format of an elasticsearch query
     * @return The response from elasticsearch
     */
    public SearchResponse search(String field, String query) {
        QueryBuilder qs = QueryBuilders.queryStringQuery("\"" + query + "\"")
                .field(field)
                .analyzeWildcard(true);
        return search(qs);
    }

    public SearchResponse search(QueryBuilder qs) {
        return client.prepareSearch(config.getIndex())
                .setTypes(LIFELOG_ANNOTATION_TYPE)
                .setQuery(qs)
                .get();
    }

    @Override
    public void close() throws Exception {
        client.close();
    }
}
