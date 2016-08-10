-- this gets us the rows in the database that we can transform into JSON
SELECT img.name "image_id", txt.annotation "text", qry.annotation "query", tag.annotation "tags", ass2.annotation "assessment_annotation", ass2.relevance "assessment_relevance" FROM images img
-- text, query and tags are easy, they only have one column for the annotation
LEFT JOIN annotated_text_images txt ON txt.image_id = img.id
LEFT JOIN annotated_query_images qry ON qry.image_id = img.id
LEFT JOIN annotated_tag_images tag ON tag.image_id = img.id
-- the database I'm using is limited to postgres 9.1, so I have to do some weird stuff for relevance assessment
LEFT JOIN (
SELECT
  DISTINCT
  -- this inner image_id is joined to the outer image_id
  image_id,
  -- we can transpose the columns into arrays (which flattens them)
  array(
      -- the id of the annotation is pretty useless so we can grab the name from the concepts table
      SELECT
        c.value
      FROM annotated_assessment_images a
        JOIN assessment_concepts c ON a.annotation = c.id
      WHERE a.image_id = ass1.image_id
  ) annotation,
  array(
      SELECT
        relevance
      FROM annotated_assessment_images a
      WHERE a.image_id = ass1.image_id
  ) relevance
  FROM annotated_assessment_images ass1) ass2 ON ass2.image_id = img.id

