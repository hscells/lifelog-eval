package com.hscells.lifelogeval.model;

/**
 * Created by Harry Scells on 10/08/2016.
 */
public class Run {

    private String queryId;
    private String documentId;
    private int rank;
    private float score;

    public Run(String queryId, String documentId, int rank, float score) {
        this.queryId = queryId;
        this.documentId = documentId;
        this.rank = rank;
        this.score = score;
    }

    @Override
    public String toString() {
        return String.format("%s\tQ0\t%s\t%d\t%f", queryId, documentId, rank, score);
    }
}
