#!/bin/bash
# New optics rendering of NeuroPump. There are 3 modes: change_background_light / change_s / change_refraction_index


export CUDA_VISIBLE_DEVICES=0

SCENES=( "pre_pg_flower910" )


NEW_BGL_R=0.5 # set 0 ~ 1
NEW_BGL_G=0.1 # set 0 ~ 1
NEW_BGL_B=0.1 # set 0 ~ 1

EXPERIMENT="test_pump_train"
DATA_DIR="data/NEW_COLMAP"


for SCENE in "${SCENES[@]}"
do
  CHECKPOINT_DIR="ckpt/test_train/${SCENE}_${EXPERIMENT}"
  CHECKPOINTS=("checkpoint_150000")

  for CHECKPOINT in "${CHECKPOINTS[@]}"
  do
    python -m render \
      --gin_configs="${CHECKPOINT_DIR}/config.gin" \
      --gin_bindings="Config.uwrays = True" \
      --gin_bindings="Config.data_dir = '${DATA_DIR}/${SCENE}'" \
      --gin_bindings="Config.checkpoint_dir = '${CHECKPOINT_DIR}/${CHECKPOINT}'" \
      --gin_bindings="Config.render_path = False" \
      --gin_bindings="Config.render_path_frames = 24" \
      --gin_bindings="Config.render_dir = '${CHECKPOINT_DIR}/test/new_bgl/set1'" \
      --gin_bindings="Config.render_new_optic = 'change_background_light'" \
      --gin_bindings="Config.n_w = 1.333" \
      --gin_bindings="Config.n_a = 1.0" \
      --gin_bindings="Config.new_bgl_r = $NEW_BGL_R" \
      --gin_bindings="Config.new_bgl_g = $NEW_BGL_G" \
      --gin_bindings="Config.new_bgl_b = $NEW_BGL_B" \
      --logtostderr
  done
  
done 