from src.opencv.getStage import getStage

def checkStage(device, expected_stage, templates, debug=False):
    stage_info = getStage(device, templates, debug=debug)

    if stage_info is None:
        raise ValueError(f"Stage check failed: expected stage {expected_stage}, but got None")

    stage, best_score = stage_info

    if debug:
        print(f"Detected stage: {stage} with certainty: {best_score:.2f}")

    if stage != expected_stage:
        raise ValueError(f"Stage check failed: expected stage {expected_stage}, but got stage {stage}")

def tryCheckStage(device, expected_stage, templates, retries=5, debug=False):
    for attempt in range(1, retries + 1):
        try:
            return checkStage(device, expected_stage, templates, debug)
        except ValueError as e:
            print(f"Attempt {attempt} for stage {expected_stage} failed: {e}")
    raise ValueError(f"Stage {expected_stage} verification failed after {retries} attempts.")
