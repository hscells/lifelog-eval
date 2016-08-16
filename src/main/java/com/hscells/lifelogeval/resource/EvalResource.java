package com.hscells.lifelogeval.resource;

import com.hscells.lifelogeval.model.experiment.Experiment;
import com.hscells.lifelogeval.service.EvalService;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;

/**
 * Created by Harry Scells on 10/08/2016.
 */
@Path("/api/eval")
public class EvalResource {

    EvalService evalService;

    public EvalResource(EvalService evalService) {
        this.evalService = evalService;
    }

    @Path("/query")
    @POST
    @Produces(MediaType.TEXT_PLAIN)
    public String postQuery(Experiment experiment) {
        return evalService.query(experiment);
    }

}
