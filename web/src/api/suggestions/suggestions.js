import { get } from "../utils";

export default {
  getSuggestions: () => get({ resource: "/suggestions"})
};
