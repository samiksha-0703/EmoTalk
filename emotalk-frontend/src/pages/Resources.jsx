import "./Resources.css";

export default function Resources() {
  return (
    <div className="resources-page">
      <header className="resources-header">
        <h2>Resources</h2>
        <p>
          Carefully selected books, audio guides, and videos to support emotional
          well-being.
        </p>
      </header>

      {/* BOOKS */}
      <section className="resource-section books">
        <h3>Books</h3>
        <div className="resource-grid">
          <ResourceCard
            title="Emotional Awareness Guide"
            description="Better Mental Health for All – Mental Health Foundation"
            link="/books/book1.pdf"
            linkText="Read PDF"
          />
          <ResourceCard
            title="Mindfulness and Mental Health"
            description="Nursing Mental Health and Community Concepts by Elizabeth Christman and Kimberly Ernstmeyer"
            link="/books/book2.pdf"
            linkText="Read PDF"
          />
          <ResourceCard
            title="Managing Stress and Anxiety"
            description="The Little Book of Mental Health"
            link="/books/book3.pdf"
            linkText="Read PDF"
          />
        </div>
      </section>

      {/* AUDIO */}
<section className="resource-section audio">
  <h3>Audio Guides</h3>
  <div className="resource-grid">
    <AudioCard
      title="Calming Breathing Exercise"
      src="/audio/audio1.mpeg"
    />
    <AudioCard
      title="Relaxation and Focus Music"
      src="/audio/audio2.mpeg"
    />
    <AudioCard
      title="Guided Meditation"
      src="/audio/audio3.mpeg"
    />
  </div>
</section>


      {/* VIDEOS */}
      <section className="resource-section videos">
        <h3>Videos</h3>
        <div className="resource-grid">
          <ResourceCard
            title="Understanding Your Emotions"
            description="Psychology backed explanation of emotions"
            link="https://www.youtube.com/watch?v=0gks6ceq4eQ"
            linkText="Watch"
          />
          <ResourceCard
            title="Mindfulness for Beginners"
            description="Simple mindfulness practices for everyday life"
            link="https://www.youtube.com/watch?v=inpok4MKVLM"
            linkText="Watch"
          />
          <ResourceCard
            title="Stress Management Techniques"
            description="Effective techniques to reduce stress"
            link="https://www.youtube.com/watch?v=ZToicYcHIOU"
            linkText="Watch"
          />
        </div>
      </section>
    </div>
  );
}

/* ---------- COMPONENTS ---------- */

function ResourceCard({ title, description, link, linkText }) {
  return (
    <div className="resource-card">
      <h4>{title}</h4>
      {description && <p className="description">{description}</p>}
      <a href={link} target="_blank" rel="noreferrer">
        {linkText}
      </a>
    </div>
  );
}

function AudioCard({ title, src }) {
  return (
    <div className="resource-card">
      <h4>{title}</h4>
      <audio controls preload="metadata" className="audio-player">
        <source src={src} type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}

