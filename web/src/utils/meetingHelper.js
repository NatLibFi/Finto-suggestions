export const getMeetingProgressionCounts = meeting => {
  if (meeting) {
    const processed = meeting.processed.length ? meeting.processed.length : 0;
    const suggestions = meeting.suggestions.length ? meeting.suggestions.length : 0;
    const progression = processed > 0 ? ((processed / suggestions) * 100).toFixed(1) : 0;
    return { processed, suggestions, progression };
  }
};

export const getMeetingProgressionWidths = progressionPercent => {
  if (progressionPercent && progressionPercent > 0) {
    return {
      progressWidth: { width: `${progressionPercent}%` },
      backgroundWidth: { width: `${100 - progressionPercent}%` }
    };
  }
  return null;
};
