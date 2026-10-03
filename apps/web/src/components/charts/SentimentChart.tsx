'use client';

export function SentimentChart() {
  const data = [42, 45, 48, 52, 55, 58, 61, 64, 62, 64];
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min;
  const width = 100;
  const height = 100;

  return (
    <svg viewBox="0 0 100 100" className="w-full h-full" aria-hidden="true" focusable="false" role="img">
      <title>Sentiment trend chart</title>
      <path
        d={data.map((v, i) => {
          const x = (i / (data.length - 1)) * width;
          const y = height - ((v - min) / range) * height * 0.8 - height * 0.1;
          return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`;
        }).join(' ')}
        fill="none"
        stroke="var(--color-positive)"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="animate-chart-draw"
        style={{ strokeDasharray: 1000, strokeDashoffset: 1000 }}
      />
      {data.map((v, i) => {
        const x = (i / (data.length - 1)) * width;
        const y = height - ((v - min) / range) * height * 0.8 - height * 0.1;
        return (
          <circle key={i} cx={x} cy={y} r="3" fill="var(--color-positive)" stroke="white" strokeWidth="2" opacity={i === data.length - 1 ? 1 : 0.6} />
        );
      })}
    </svg>
  );
}