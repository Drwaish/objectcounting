""" Live and Recoded video Processing"""
import supervision as sv
from tqdm.notebook import tqdm
import functionality.model as model

model = model.load_model()
object_count = []

def process_live(frame):
    """
    In this method live video processing will be done.

    Parameters
    ----------
    frame
      Image capture by web cam

    Return
    ------
    Image
      Return the process image realtime.
    """
    results = model(frame)[0]
    byte_tracker = sv.ByteTrack()
    detections = sv.Detections.from_ultralytics(results)
    annotator = sv.BoxAnnotator()
    detections = byte_tracker.update_with_detections(detections)
    labels = [
         f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
         for _, _, confidence, class_id, tracker_id
         in detections
    ]
    with open("subtitles.txt","a", encoding= "utf-8") as file:
        file.writelines(str(labels) + '\n' + '\n')
    ids = detections.class_id
    for id in ids:
        object_count.append(id)
    yield (annotator.annotate(scene=frame, detections=detections, labels=labels), len(object_count))

def process_video(SOURCE_VIDEO_PATH):
    """
    In this method video processing will be done.

    Parameters
    ----------
    SOURCE_VIDEO_PATH
        Video to detect track and count object

    Return
    ------
    Image
        Return the process frame .
    """
    # create BYTETracker instance
    byte_tracker = sv.ByteTrack()
    video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
    # create frame generator
    generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)
    # create LineCounter instance
    # create instance of BoxAnnotator and LineCounterAnnotator
    box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
    print("Video Info :", video_info)
    # open target video file
        # loop over video frames
    for frame in tqdm(generator, total=video_info.total_frames):
        # model prediction on single frame and conversion to supervision Detections
        results = model(frame)
        # detections = sv.Detections.from_ultralytics(results)
        detections = sv.Detections(
        xyxy=results[0].boxes.xyxy.cpu().numpy(),
        confidence=results[0].boxes.conf.cpu().numpy(),
        class_id=results[0].boxes.cls.cpu().numpy().astype(int)
    )
        detections = byte_tracker.update_with_detections(detections)
        labels = [
            f"#{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, tracker_id
            in detections
        ]
        with open("subtitles.txt","a", encoding='utf-8') as file:
            file.writelines(str(labels) + '\n' + '\n')
        ids = detections.class_id
        for id in ids:
            if object_count.count(id) == 0 :
                object_count.append(id)
        yield (box_annotator.annotate(scene=frame, detections=detections, labels=labels), len(object_count))
