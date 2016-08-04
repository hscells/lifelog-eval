package com.hscells.lifelogeval.service;

import com.hscells.lifelogeval.config.ElasticSearchConfiguration;
import com.hscells.lifelogeval.model.LifelogDocument;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.xcontent.XContentType;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Harry Scells on 2/08/2016.
 */
public class ElasticSearchService implements AutoCloseable {

    private ElasticSearchConfiguration config;
    private Client client;

    private static final String INDEX_NAME = "lifelog";

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
        document.put("timestamp", lifelogDocument.getTimestamp());
        document.put("location", lifelogDocument.getLocation());
        document.put("activity", lifelogDocument.getActivity());
        for (String key : lifelogDocument.getAnnotations().keySet()) {
            document.put(key, lifelogDocument.getAnnotations().get(key));
        }
        return document;
    }

    /**
     * Add a lifelog image to the index
     * @param lifelogDocument
     * @return The response from elasticsearch
     */
    public IndexResponse indexDocument(LifelogDocument lifelogDocument) {
        Map<String, Object> document = transformDocument(lifelogDocument);
        return client.prepareIndex(config.getIndex(), INDEX_NAME, lifelogDocument.getId())
                .setSource(document)
                .setContentType(XContentType.JSON)
                .get();
    }

    /**
     * Get a specific document from the index by its id
     * @param id
     * @return The response from elasticsearch
     */
    public GetResponse getDocument(String id) {
        return client.prepareGet(config.getIndex(), INDEX_NAME, id).get();
    }

    /**
     * Submit a standard elasticsearch query
     * @param query A JSON string in the format of an elasticsearch query
     * @return The response from elasticsearch
     */
    public SearchResponse search(String query) {
        return client.prepareSearch(config.getIndex())
                .setTypes(INDEX_NAME)
                .setSearchType(SearchType.DFS_QUERY_AND_FETCH)
                .setQuery(query)
                .execute()
                .actionGet();
    }

    @Override
    public void close() throws Exception {
        client.close();
    }
}
