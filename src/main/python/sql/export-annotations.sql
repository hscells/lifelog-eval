-- this gets us the rows in the database that we can transform into JSON
SELECT img.name "image_id", txt.annotation "text", qry.annotation "query", tag.annotation "tags", ass2.annotation "assessment_annotation", ass2.relevance "assessment_relevance" FROM images img
  -- text, query and tags are easy, they only have one column for the annotation
  LEFT JOIN annotated_text_images txt ON txt.image_id = img.id
  LEFT JOIN annotated_query_images qry ON qry.image_id = img.id
  LEFT JOIN annotated_tag_images tag ON tag.image_id = img.id
  -- the database I'm using is limited to postgres 9.1, so I have to do some weird stuff for relevance assessment
  LEFT JOIN (
    SELECT image_id, array(
       SELECT c.value
       FROM assessment_concepts c
         JOIN unnest(annotation) a ON a = c.id
    ) annotation, relevance FROM (
      SELECT DISTINCT image_id, array_agg(annotation) annotation, array_agg(relevance) relevance
      FROM annotated_assessment_images
      GROUP BY image_id
    ) x) ass2 ON ass2.image_id = img.id
-- finally, just skip any images where there are no annotations at all
WHERE txt.annotation IS NOT NULL OR qry.annotation IS NOT NULL OR tag.annotation IS NOT NULL OR ass2.annotation IS NOT NULL;