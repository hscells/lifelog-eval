package com.hscells.lifelogeval.model;

import java.util.Map;

/**
 * Created by Harry Scells on 2/08/2016.
 * This must be generic. Evaluation should be able to be performed on an arbitrary
 * set of annotation methodologies, and these methodologies can vary in the way they
 * are stored (the data structure) and the way they are retrieved by the search engine.
 */
public class LifelogDocument {

    private String id;
    private Map<String, Object> annotations;

    public LifelogDocument() {
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Map<String, Object> getAnnotations() {
        return annotations;
    }

    public void setAnnotations(Map<String, Object> annotations) {
        this.annotations = annotations;
    }
}
