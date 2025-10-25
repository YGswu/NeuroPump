#!/bin/bash
# New optics rendering of NeuroPump. There are 3 modes: change_background_light / change_s / change_refraction_index


export CUDA_VISIBLE_DEVICES=0

SCENES=( "pre_pg_flower910" )


EXPERIMENT="test_pump_train"
DATA_DIR="data/NEW_COLMAP"


for SCENE in "${SCENES[@]}"
do

  CHECKPOINT_DIR="ckpt/test_train/${SCENE}_${EXPERIMENT}"
  CHECKPOINTS=("checkpoint_150000")


  for CHECKPOINT in "${CHECKPOINTS[@]}"
  do
  
    START_N=0.9
    END_N=2.00
    STEP=0.05

    
    for N in $(seq $START_N $STEP $END_N)
    do
      
      python -m render \
        --gin_configs="${CHECKPOINT_DIR}/config.gin" \
        --gin_bindings="Config.data_dir = '${DATA_DIR}/${SCENE}'" \
        --gin_bindings="Config.checkpoint_dir = '${CHECKPOINT_DIR}/${CHECKPOINT}'" \
        --gin_bindings="Config.render_path = False" \
        --gin_bindings="Config.render_path_frames = 24" \
        --gin_bindings="Config.render_dir = '${CHECKPOINT_DIR}/test/RI/$N'" \
        --gin_bindings="Config.render_video_fps = 5" \
        --gin_bindings="Config.render_new_optic = 'change_refraction_index'" \
        --gin_bindings="Config.n_w = $N" \
        --logtostderr
    done
  
  done

done