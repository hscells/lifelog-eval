./run-judged-experiment.sh ntcir_data/lifelogging_topics_formal.xml ntcir_data/ntcir12_lifelog_lsat_image_qrels.txt kaparthy-captions_combined.json && mv ./experiments/judged-experiment.txt ./experiments/karpathy_learnt_judged-experiment.txt && mv ./experiments/judged-experiment.eval.txt ./experiments/karpathy_learnt_judged-experiment.eval.txt &&
./run-judged-experiment.sh ntcir_data/lifelogging_topics_formal.xml ntcir_data/ntcir12_lifelog_lsat_image_qrels.txt sample+rel-learnt_combined.json && mv ./experiments/judged-experiment.txt ./experiments/sample+rel-learnt_combined_judged-experiment.txt && mv ./experiments/judged-experiment.eval.txt ./experiments/sample+rel-learnt_combined_judged-experiment.eval.txt &&
./run-judged-experiment.sh ntcir_data/lifelogging_topics_formal.xml ntcir_data/ntcir12_lifelog_lsat_image_qrels.txt sample-learnt_combined.json  && mv ./experiments/judged-experiment.txt ./experiments/sample-learnt_combined_judged-experiment.txt && mv ./experiments/judged-experiment.eval.txt ./experiments/sample-learnt_combined_judged-experiment.eval.txt &&

./run-judged-experiment.sh ntcir_data/lifelogging_topics_formal.xml ntcir_data/ntcir12_lifelog_lsat_image_qrels.txt karpathy_caption_annotations.json && mv ./experiments/judged-experiment.txt ./experiments/karpathy_caption_annotations_judged-experiment.txt && mv ./experiments/judged-experiment.eval.txt ./experiments/karpathy_caption_annotations_judged-experiment.eval.txt &&
./run-judged-experiment.sh ntcir_data/lifelogging_topics_formal.xml ntcir_data/ntcir12_lifelog_lsat_image_qrels.txt sample+rel_learnt_caption_annotations.json && mv ./experiments/judged-experiment.txt ./experiments/sample+rel_learnt_caption_annotations_judged-experiment.txt && mv ./experiments/judged-experiment.eval.txt ./experiments/sample+rel_learnt_caption_annotations_judged-experiment.eval.txt &&
./run-judged-experiment.sh ntcir_data/lifelogging_topics_formal.xml ntcir_data/ntcir12_lifelog_lsat_image_qrels.txt sample_learnt_caption_annotations.json  && mv ./experiments/judged-experiment.txt ./experiments/sample_learnt_caption_annotations_judged-experiment.txt && mv ./experiments/judged-experiment.eval.txt ./experiments/sample_learnt_caption_annotations_judged-experiment.eval.txt &&

ntfy send "finished running experiments"
