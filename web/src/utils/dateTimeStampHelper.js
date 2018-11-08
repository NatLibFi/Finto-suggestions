import { differenceInDays, parse } from 'date-fns';

export const dateDiffLabel = createdDate => {
  const whenSended = differenceInDays(parse(new Date()), parse(createdDate));
  return whenSended > 0 ? `${whenSended} päivää sitten` : 'tänään';
};
