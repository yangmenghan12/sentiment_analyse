from modelscope import snapshot_download

local_dir = snapshot_download(model_id="", local_dir="")

print(local_dir)