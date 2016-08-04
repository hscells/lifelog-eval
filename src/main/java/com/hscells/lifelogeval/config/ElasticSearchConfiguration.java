package com.hscells.lifelogeval.config;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Created by Harry Scells on 2/08/2016.
 */
public class ElasticSearchConfiguration {

    @JsonProperty
    private String url;

    @JsonProperty
    private String username;

    @JsonProperty
    private String password;

    @JsonProperty
    private String index;

    @JsonProperty
    private String cluster;

    public ElasticSearchConfiguration(){}

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getIndex() {
        return index;
    }

    public void setIndex(String index) {
        this.index = index;
    }

    public String getCluster() {
        return cluster;
    }

    public void setCluster(String cluster) {
        this.cluster = cluster;
    }
}
