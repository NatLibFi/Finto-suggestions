import { suggestionStateStatus } from './suggestionHelpers.js';

/*
 * Local method for calculating processed suggestions count
 */
const getProcessedCount = processed => {
  let count = 0;

  if (processed) {
    const accepted = processed[suggestionStateStatus.ACCEPTED];
    const retained = processed[suggestionStateStatus.RETAINED];
    const rejected = processed[suggestionStateStatus.REJECTED];

    if (accepted && accepted > 0) {
      count += accepted;
    }

    if (retained && retained > 0) {
      count += retained;
    }

    if (rejected && rejected > 0) {
      count += rejected;
    }
  }
  return count;
};

export const getMeetingProgressionCounts = meeting => {
  if (meeting) {
    const processed = getProcessedCount(meeting.processed);
    const suggestions =
      meeting.suggestions && meeting.suggestions.length > 0 ? meeting.suggestions.length : 0;
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
