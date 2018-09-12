import { get } from "../utils";

export default {
  getSuggestions: () => get({ resource: "/suggestions" }),
  getAllNewSuggestions: () =>
    get({ resource: "/suggestions?filters=type%3Anew" }),
  getAllResolvedSuggestions: () =>
    get({
      resource: "/suggestions?filters=status%3AACCEPTED%7Cstatus%3AREJECTED"
    }),
  getSortedSuggestions: sortValue =>
    get({ resource: `/suggestions?sort=${sortValue}` })
};
