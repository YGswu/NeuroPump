#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

SCENES=("pre_pg_flower910")

EXPERIMENT="test_pump_train"
DATA_DIR="data/NEW_COLMAP"

for SCENE in "${SCENES[@]}"
do
  SCENE="$SCENE"

  CHECKPOINT_DIR="ckpt/test_train/"$SCENE"_"$EXPERIMENT""

  CHECKPOINTS=("150000")

  for CHECKPOINT in "${CHECKPOINTS[@]}"
  do
    python -m render \
      --gin_configs="${CHECKPOINT_DIR}/config.gin" \
      --gin_bindings="Config.uwrays = False" \
      --gin_bindings="Config.data_dir = '${DATA_DIR}/${SCENE}'" \
      --gin_bindings="Config.checkpoint_dir = '${CHECKPOINT_DIR}/checkpoint_${CHECKPOINT}'" \
      --gin_bindings="Config.render_path = False" \
      --gin_bindings="Config.render_dir = '${CHECKPOINT_DIR}/renders'" \
      --gin_bindings="Config.render_scene = '${SCENE}'" \
      --gin_bindings="Config.render_new_optic = 'no'" \
      --gin_bindings="Config.parent_folder = '${CHECKPOINT_DIR}/renders/render_step_${CHECKPOINT}'" \
      --logtostderr
  done
done