from src.opencv.getStage import getStage

def checkStage(device, expected_stage, templates, debug=False):
    stage = getStage(device, templates, debug)
    if stage != expected_stage:
        raise ValueError(f"Stage check failed: expected stage {expected_stage}, but got stage {stage}")

def tryCheckStage(device, expected_stage, templates, retries=5):
    for attempt in range(1, retries + 1):
        try:
            checkStage(device, expected_stage, templates)
            return
        except ValueError as e:
            print(f"Attempt {attempt} for stage {expected_stage} failed: {e}")
    raise ValueError(f"Stage {expected_stage} verification failed after {retries} attempts.")