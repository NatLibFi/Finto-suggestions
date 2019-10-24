import { differenceInDays, parse, format, isAfter } from 'date-fns';

export const formatDate = (date, formatting) => {
  return format(parse(date), formatting);
};

export const hasDatePassed = date => {
  return isAfter(new Date(), format(date, 'DD.MM.YYYY'));
};

/*
 * Params: date to make formating as Datetime
 * Formats date format as 'Lähetetty x päivää sitten'
 * or when it's over 30 just sends 'Lähetetty dd.MM.YYYY'
 */
export const dateTimeFormatLabel = (date, isMeeting = false) => {
  const whenSended = differenceInDays(parse(new Date()), parse(date));
  if (!isMeeting) {
    if (whenSended === 0) {
      // return `Lähetetty tänään`;
      return `Lähetetty ${format(date, 'DD.MM.YYYY')}`;
    }
    if (whenSended === 1) {
      // return `Lähetetty eilen`;
      return `Lähetetty ${format(date, 'DD.MM.YYYY')}`;
    }
    return whenSended > 1 && whenSended < 30
      // ? `Lähetetty ${whenSended} päivää sitten`
      ? `Lähetetty ${format(date, 'DD.MM.YYYY')}`
      : `Lähetetty ${format(date, 'DD.MM.YYYY')}`;
  }
  if (isMeeting) {
    return format(date, 'DD.MM.YYYY');
  }
};
