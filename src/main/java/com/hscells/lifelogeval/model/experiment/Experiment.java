package com.hscells.lifelogeval.model.experiment;

import java.util.List;

/**
 * Created by Harry Scells on 16/08/2016.
 */
public class Experiment {

    private List<String> fields;
    private List<Topic> topics;
    private String name;

    public Experiment() {
    }

    public List<String> getFields() {
        return fields;
    }

    public void setFields(List<String> fields) {
        this.fields = fields;
    }

    public List<Topic> getTopics() {
        return topics;
    }

    public void setTopics(List<Topic> topics) {
        this.topics = topics;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
