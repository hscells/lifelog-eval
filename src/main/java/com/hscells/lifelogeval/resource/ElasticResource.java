package com.hscells.lifelogeval.resource;

import com.hscells.lifelogeval.model.LifelogDocument;
import com.hscells.lifelogeval.service.ElasticSearchService;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.search.SearchHit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

/**
 * Created by Harry Scells on 4/08/2016.
 */
@Path("/api/elastic")
public class ElasticResource {

    private static final Logger logger = LoggerFactory.getLogger(ElasticResource.class);

    private ElasticSearchService elasticSearchService;

    public ElasticResource(ElasticSearchService elasticSearchService) {
        this.elasticSearchService = elasticSearchService;
    }

    @Path("/index")
    @POST
    public void postDocuments(List<LifelogDocument> documents) {
        elasticSearchService.indexDocuments(documents);
    }

    @Path("/index")
    @DELETE
    public boolean deleteDocuments() throws ExecutionException, InterruptedException {
        return elasticSearchService.deleteIndex();
    }

    @Path("/get/{id}")
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Map<String, Object> postDocument(@PathParam("id") String id) {
        return elasticSearchService.getDocument(id).getSource();
    }

    @Path("/search/{field}/{query}")
    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<Map<String, Object>> searchDocuments(@PathParam("field") String field, @PathParam("query") String query) {
        SearchResponse response = elasticSearchService.search(field, query);
        SearchHit[] hits = response.getHits().hits();
        List<Map<String, Object>> result = new ArrayList<>();
        for (SearchHit hit : hits) {
            result.add(hit.getSource());
        }
        return result;
    }

}
