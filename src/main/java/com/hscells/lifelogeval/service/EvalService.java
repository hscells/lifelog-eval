package com.hscells.lifelogeval.service;

import com.hscells.lifelogeval.model.Run;
import com.hscells.lifelogeval.model.experiment.Experiment;
import com.hscells.lifelogeval.model.experiment.Topic;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.index.query.QueryStringQueryBuilder;
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

    public String query(Experiment experiment) {
        String results = "";

        for (Topic topic : experiment.getTopics()) {
            QueryStringQueryBuilder query = QueryBuilders.queryStringQuery("\"" + topic.getQuery() + "\"");

            for (String field : experiment.getFields()) {
                query = query.field(field);
            }

            SearchResponse response = elasticSearchService.search(query);
            if (response.getHits().getHits().length > 0) {
                List<Run> run = new ArrayList<>();
                final int[] i = {0};
                response.getHits().forEach(hit -> {
                    run.add(new Run(topic.getQueryId(), hit.getId(), i[0]++, hit.getScore(), topic.getDescription()));
                });
                results += run.stream().map(Run::toString).collect(Collectors.joining("\n")) + "\n";
            }
        }

        return results;
    }

}
