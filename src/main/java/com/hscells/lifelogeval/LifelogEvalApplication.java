package com.hscells.lifelogeval;

import com.hscells.lifelogeval.config.ElasticSearchConfiguration;
import com.hscells.lifelogeval.config.LifeogEvalApplicationConfiguration;
import com.hscells.lifelogeval.resource.ElasticResource;
import com.hscells.lifelogeval.resource.EvalResource;
import com.hscells.lifelogeval.service.ElasticSearchService;
import com.hscells.lifelogeval.service.EvalService;
import io.dropwizard.Application;
import io.dropwizard.configuration.EnvironmentVariableSubstitutor;
import io.dropwizard.configuration.SubstitutingSourceProvider;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;

/**
 * Created by Harry Scells on 2/08/2016.
 */
public class LifelogEvalApplication extends Application<LifeogEvalApplicationConfiguration> {

    @Override
    public void run(LifeogEvalApplicationConfiguration configuration, Environment environment) throws Exception {

        final ElasticSearchConfiguration elasticSearchConfiguration = configuration.getElasticSearchConfiguration();

        final ElasticSearchService elasticSearchService = new ElasticSearchService(elasticSearchConfiguration);
        final EvalService evalService = new EvalService(elasticSearchService);

        environment.jersey().register(new ElasticResource(elasticSearchService));
        environment.jersey().register(new EvalResource(evalService));
    }

    @Override
    public void initialize(Bootstrap<LifeogEvalApplicationConfiguration> bootstrap) {
        bootstrap.setConfigurationSourceProvider(
                new SubstitutingSourceProvider(bootstrap.getConfigurationSourceProvider(),
                        new EnvironmentVariableSubstitutor(/* strict? */ false))
        );
    }

    public static void main(String[] args) throws Exception {
        new LifelogEvalApplication().run(args);
    }
}
