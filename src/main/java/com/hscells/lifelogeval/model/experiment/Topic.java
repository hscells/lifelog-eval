package com.hscells.lifelogeval.model.experiment;

/**
 * Created by Harry Scells on 16/08/2016.
 */
public class Topic {

    private String queryId;
    private String query;
    private String description;

    public Topic() {
    }

    public String getQueryId() {
        return queryId;
    }

    public void setQueryId(String queryId) {
        this.queryId = queryId;
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
