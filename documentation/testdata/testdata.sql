-- Creates meetings
BEGIN;
INSERT INTO public.meetings(name, created, modified, meeting_date)
VALUES ('Test meeting', localtimestamp, localtimestamp, localtimestamp + interval '7' day);

INSERT INTO public.meetings(name, created, modified, meeting_date)
VALUES ('Another test meeting', localtimestamp, localtimestamp, localtimestamp + interval '30' day);

-- Creates suggestions
INSERT INTO public.suggestions(created, modified, suggestion_type, status, uri, organization, description, reason, preferred_label, alternative_label, broader, narrower, related, "group", meeting_id) 
VALUES (localtimestamp - interval '7' day, localtimestamp, 'NEW', null, 'QWERTY', 'TestOrg', 'Testdata for testing the webapp', 'Testing the app', '{ "fi": "Testdata for testing the webapp" }', '{}', '{}', '{}', '{}', '{}', 1);

INSERT INTO public.suggestions(created, modified, suggestion_type, status, uri, organization, description, reason, preferred_label, alternative_label, broader, narrower, related, "group", meeting_id) 
VALUES (localtimestamp - interval '7' day, localtimestamp, 'NEW', null, 'QWERTY', 'TestOrg', 'More testdata for testing the webapp', 'Testing the app', '{ "fi": "More testdata for testing the webapp"} ', '{}', '{}', '{}', '{}', '{}', 2);

-- Creates test tags
INSERT INTO public.tags(label) VALUES ('TestTag_1');
INSERT INTO public.tags(label) VALUES ('TestTag_2');
INSERT INTO public.tags(label) VALUES ('TestTag_3');
INSERT INTO public.tags(label) VALUES ('TestTag_4');
INSERT INTO public.tags(label) VALUES ('TestTag_5');

-- Creates one default user
INSERT INTO public.users(created, name, email, role, password_hash)
VALUES(localtimestamp, 'Test User', 'testuser@user.com', 'NORMAL', '$pbkdf2-sha256$29000$fa8Vwtj7/7.3VirlnFNqzQ$A4g8TIfe4DdVqEsFzC6fReehzZ.AX0Yjgp1ql8u//yA');

-- Creates one action type event
INSERT INTO public.events(created, modified, event_type, text, suggestion_id, user_id)
VALUES(localtimestamp, localtimestamp, 'ACTION', 'test action event', 1, 1);

-- Associates tags to suggestions
INSERT INTO public.suggestion_tags_association(tag_label, suggestion_id) VALUES('TestTag_1', 1);
INSERT INTO public.suggestion_tags_association(tag_label, suggestion_id) VALUES('TestTag_2', 1);
INSERT INTO public.suggestion_tags_association(tag_label, suggestion_id) VALUES('TestTag_1', 2);
INSERT INTO public.suggestion_tags_association(tag_label, suggestion_id) VALUES('TestTag_2', 2);
COMMIT;
