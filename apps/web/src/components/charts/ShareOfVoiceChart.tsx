'use client';

export function ShareOfVoiceChart() {
  const segments = [
    { label: 'Zomato', value: 28.4, color: 'var(--color-accent)' },
    { label: 'Swiggy', value: 35.2, color: 'var(--color-text-secondary)' },
    { label: 'Others', value: 36.4, color: 'var(--color-border)' },
  ];

  let startAngle = -90;

  return (
    <svg viewBox="0 0 100 100" className="w-full h-full" aria-hidden="true" focusable="false" role="img">
      <title>Share of voice chart</title>
      <g>
        {segments.map((seg, i) => {
          const angle = (seg.value / 100) * 360;
          const endAngle = startAngle + angle;
          const startRad = (startAngle * Math.PI) / 180;
          const endRad = (endAngle * Math.PI) / 180;
          const x1 = 50 + 40 * Math.cos(startRad);
          const y1 = 50 + 40 * Math.sin(startRad);
          const x2 = 50 + 40 * Math.cos(endRad);
          const y2 = 50 + 40 * Math.sin(endRad);
          const largeArc = angle > 180 ? 1 : 0;

          startAngle = endAngle;

          return (
            <path
              key={i}
              d={`M 50 50 L ${x1} ${y1} A 40 40 0 ${largeArc} 1 ${x2} ${y2} Z`}
              fill={seg.color}
              stroke="var(--color-background)"
              strokeWidth="2"
              className="animate-chart-draw"
              style={{ animationDelay: `${i * 150}ms` }}
            />
          );
        })}
      </g>
      <circle cx="50" cy="50" r="28" fill="var(--color-background)" />
      <text x="50" y="48" textAnchor="middle" className="font-mono font-bold" fontSize="16" fill="var(--color-ink)">
        28.4%
      </text>
      <text x="50" y="66" textAnchor="middle" className="font-sans text-xs" fontSize="9" fill="var(--color-text-muted)">
        Your Share
      </text>
    </svg>
  );
}