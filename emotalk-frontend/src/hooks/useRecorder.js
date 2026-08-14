import { useReactMediaRecorder } from "react-media-recorder";

export default function useRecorder() {
  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  } = useReactMediaRecorder({ audio: true });

  return {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  };
}
