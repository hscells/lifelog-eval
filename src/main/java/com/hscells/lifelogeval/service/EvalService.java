package com.hscells.lifelogeval.service;

import com.hscells.lifelogeval.model.Run;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.search.SearchHitField;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Created by Harry Scells on 10/08/2016.
 */
public class EvalService {

    private ElasticSearchService elasticSearchService;

    private static final Logger logger = LoggerFactory.getLogger(EvalService.class);

    public EvalService(ElasticSearchService elasticSearchService) {
        this.elasticSearchService = elasticSearchService;
    }

    public String query(String field, String query) {
        SearchResponse response = elasticSearchService.search(field, query);
        List<Run> run = new ArrayList<>();
        final int[] i = {0};
        response.getHits().forEach(hit -> {
            run.add(new Run(field, hit.getId(), i[0]++ , hit.getScore()));
        });
        return run.stream().map(Run::toString).collect(Collectors.joining("\n"));
    }

}
