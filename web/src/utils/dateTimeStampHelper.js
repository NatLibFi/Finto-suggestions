import { differenceInDays, parse, format } from 'date-fns';

/*
* Params: date to make formating as Datetime
* Formats date format as 'Lähetetty x päivää sitten'
* or when it's over 30 just sends 'Lähetetty dd.MM.YYYY'
*/
export const dateTimeFormatLabel = date => {
  const whenSended = differenceInDays(parse(new Date()), parse(date));
  return whenSended > 0 && whenSended < 30
    ? `Lähetetty ${whenSended} päivää sitten`
    : `Lähetetty ${format(date, 'DD.MM.YYYY')}`;
};
