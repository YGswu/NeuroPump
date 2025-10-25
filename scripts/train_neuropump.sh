#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
export WANDB_MODE="disabled"  # Set "online" to open wandb

SCENES=("pre_pg_flower910") # You can set all 5 scenes here

for SCENE in "${SCENES[@]}"
do
  SCENE="$SCENE"
  EXPERIMENT=test_pump_train
  DATA_DIR=data/NEW_COLMAP
  CHECKPOINT_DIR=ckpt/test_train/"$SCENE"_"$EXPERIMENT"
  

  if [ "$SCENE" == "pre_pg_flower910" ]; then
    R_AVG=75.0347  
    G_AVG=96.9022  
    B_AVG=69.6753  
  elif [ "$SCENE" == "pre_pg_hero910" ]; then
    R_AVG=93.3337  
    G_AVG=121.9189  
    B_AVG=95.6066  
  elif [ "$SCENE" == "pre_totoro910" ]; then
    R_AVG=128.3210  
    G_AVG=148.4776  
    B_AVG=150.2212  
  elif [ "$SCENE" == "pre_lying_cow910" ]; then
    R_AVG=103.0820  
    G_AVG=120.8609  
    B_AVG=84.7241  
  elif [ "$SCENE" == "pre_org910" ]; then
    R_AVG=120.8526 
    G_AVG=93.3523 
    B_AVG=72.8314 
  fi
    

  python -m train \
    --gin_configs=configs/train_neuropump.gin \
    --gin_bindings="Config.factor = 2" \
    --gin_bindings="Config.batch_size = 2048" \
    --gin_bindings="Config.max_steps = 150000" \
    --gin_bindings="Config.lr_init = 0.00025" \
    --gin_bindings="Config.lr_final = 0.000025" \
    --gin_bindings="Config.checkpoint_every = 10000" \
    --gin_bindings="Config.data_dir = '${DATA_DIR}/${SCENE}'" \
    --gin_bindings="Config.checkpoint_dir = '${CHECKPOINT_DIR}'" \
    --gin_bindings="Config.r_avg = ${R_AVG}" \
    --gin_bindings="Config.g_avg = ${G_AVG}" \
    --gin_bindings="Config.b_avg = ${B_AVG}" \
    --gin_bindings="Config.n_w = 1.333" \
    --gin_bindings="Config.n_a = 1.0" \
    --gin_bindings="Config.uwrays = True" \
    --gin_bindings="Config.render_new_optic = False" \
    --logtostderr
done

