package com.hscells.lifelogeval.config;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.dropwizard.Configuration;
import org.hibernate.validator.constraints.NotEmpty;

import javax.validation.constraints.NotNull;

/**
 * Created by Harry Scells on 2/08/2016.
 */
public class LifeogEvalApplicationConfiguration extends Configuration {

    @JsonProperty
    private ElasticSearchConfiguration elasticSearchConfiguration;

    @JsonProperty("elastic")
    public ElasticSearchConfiguration getElasticSearchConfiguration() {
        return elasticSearchConfiguration;
    }

}
