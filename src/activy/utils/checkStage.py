from src.activy.utils.getStage import getStage

# the expected_stage can also be a table of stages
def checkStage(device, expected_stage, templates, debug=False):
    stage_info = getStage(device, templates, debug=debug)
    if stage_info is None:
        raise ValueError(f"Stage check failed: expected stage(s) {expected_stage}, but got None")

    detected_stage, best_score = stage_info

    if debug:
        print(f"Detected stage: {detected_stage} with certainty: {best_score:.2f}")

    if not isinstance(expected_stage, (list, tuple)):
        expected_stage = [str(expected_stage)]
    expected_stage = [str(item) for item in expected_stage]

    if detected_stage not in expected_stage:
        raise ValueError(f"Stage check failed: expected one of {expected_stage}, but got stage {detected_stage}")

    return stage_info


def tryCheckStage(device, expected_stage, templates, retries=10, debug=False):
    for attempt in range(1, retries + 1):
        try:
            return checkStage(device, expected_stage, templates, debug)
        except ValueError as e:
            print(f"Attempt {attempt} for stage {expected_stage} failed: {e}")
    raise ValueError(f"Stage {expected_stage} verification failed after {retries} attempts.")
