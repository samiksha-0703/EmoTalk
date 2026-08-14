export default function RecordButton({ status, onStart, onStop }) {
    return (
      <button
        onClick={status === "recording" ? onStop : onStart}
        style={{
          padding: "15px 30px",
          fontSize: "16px",
          background: status === "recording" ? "red" : "green",
          color: "white",
          border: "none",
          borderRadius: "8px",
        }}
      >
        {status === "recording" ? "Stop Recording" : "Start Recording"}
      </button>
    );
  }
  