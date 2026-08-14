function getSummary(history) {
    const total = history.length;
    const counts = {};
  
    history.forEach((item) => {
      counts[item.emotion] = (counts[item.emotion] || 0) + 1;
    });
  
    let topEmotion = null;
    let max = 0;
    for (const emotion in counts) {
      if (counts[emotion] > max) {
        max = counts[emotion];
        topEmotion = emotion;
      }
    }
  
    return { total, counts, topEmotion };
  }
  
  function getInsight(topEmotion) {
    if (!topEmotion) return "No emotional data available yet.";
  
    const map = {
      happy: "You experienced more positive moments today. Keep nurturing what supports this feeling.",
      sad: "You may have felt emotionally low at times. Gentle care and rest can help restore balance.",
      angry: "Strong emotions appeared today. Slowing down may help create ease.",
      calm: "Your emotions appear steady and balanced today.",
      fear: "You may have felt unsettled at moments. Grounding activities can be helpful.",
    };
  
    return map[topEmotion] || "Your emotional pattern shows meaningful variations today.";
  }
  
  export default function EmotionReport({ history }) {
    const { total, counts, topEmotion } = getSummary(history);
  
    return (
      <div style={{ marginTop: 20 }}>
        <p><strong>Total recordings:</strong> {total}</p>
  
        <p>
          <strong>Most frequent emotion:</strong>{" "}
          {topEmotion || "N/A"}
        </p>
  
        <h4>Emotion Breakdown</h4>
  
        {Object.entries(counts).map(([emotion, count]) => (
          <div
            key={emotion}
            style={{
              padding: "8px 12px",
              border: "1px solid #ddd",
              borderRadius: 6,
              marginBottom: 8,
            }}
          >
            {emotion} : {count}
          </div>
        ))}
  
        <h4>Insight</h4>
        <p>{getInsight(topEmotion)}</p>
      </div>
    );
  }
  