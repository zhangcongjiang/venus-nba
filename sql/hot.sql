INSERT INTO public.hot_news ("msg", "type", "rank", "author", "hots", "created_at", "category")
SELECT DISTINCT ON ("msg") "msg", "type", "rank", "author", "hots", "time"::timestamp, "category"
FROM hot_search.hot_news
WHERE "time"::timestamp  <  '2023-07-05 11:00:00'
ORDER by "msg","id";

CREATE TABLE public.hot_community (
	id bigserial NOT NULL,
	msg text NULL,
	"rank" int8 NULL,
	author varchar(32) NULL,
	category varchar(32) NULL,
	hots varchar(64) NULL,
	"type" varchar(32) NULL,
	created_at TIMESTAMP DEFAULT current_timestamp,
	CONSTRAINT hot_community_pkey PRIMARY KEY (id)
);

SELECT COUNT(DISTINCT "msg") FROM hot_search.hot_news WHERE "time"::timestamp  <  '2023-06-29 00:00:00';
