--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: administrator; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.administrator (
    id integer NOT NULL,
    username character varying(20) NOT NULL,
    password character varying(20) NOT NULL
);


ALTER TABLE public.administrator OWNER TO postgres;

--
-- Name: administrator_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.administrator_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.administrator_id_seq OWNER TO postgres;

--
-- Name: administrator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.administrator_id_seq OWNED BY public.administrator.id;


--
-- Name: class_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class_type (
    type character(2) NOT NULL,
    name character varying(25)
);


ALTER TABLE public.class_type OWNER TO postgres;

--
-- Name: classroom; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.classroom (
    id integer NOT NULL,
    building character(1) NOT NULL,
    roomnumber integer NOT NULL,
    capacity integer NOT NULL
);


ALTER TABLE public.classroom OWNER TO postgres;

--
-- Name: classroom_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.classroom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.classroom_id_seq OWNER TO postgres;

--
-- Name: classroom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.classroom_id_seq OWNED BY public.classroom.id;


--
-- Name: course_catalog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course_catalog (
    sln integer NOT NULL,
    name character varying(20) NOT NULL,
    coursecredits integer NOT NULL,
    type character(2) NOT NULL
);


ALTER TABLE public.course_catalog OWNER TO postgres;

--
-- Name: course_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course_info (
    id integer NOT NULL,
    sln integer NOT NULL,
    section character(1) NOT NULL,
    roomid integer NOT NULL,
    instructorname integer NOT NULL,
    "time" time without time zone NOT NULL,
    quarter character(2) NOT NULL,
    year integer NOT NULL
);


ALTER TABLE public.course_info OWNER TO postgres;

--
-- Name: course_info_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.course_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.course_info_id_seq OWNER TO postgres;

--
-- Name: course_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.course_info_id_seq OWNED BY public.course_info.id;


--
-- Name: note; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.note (
    id integer NOT NULL,
    note character varying(100) NOT NULL,
    date timestamp without time zone NOT NULL,
    type character(1) NOT NULL,
    adminid integer NOT NULL
);


ALTER TABLE public.note OWNER TO postgres;

--
-- Name: note_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.note_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.note_id_seq OWNER TO postgres;

--
-- Name: note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.note_id_seq OWNED BY public.note.id;


--
-- Name: note_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.note_type (
    type character(1) NOT NULL,
    name character varying(25) NOT NULL
);


ALTER TABLE public.note_type OWNER TO postgres;

--
-- Name: quarter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quarter (
    type character(2) NOT NULL,
    name character varying(25)
);


ALTER TABLE public.quarter OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    id integer NOT NULL,
    firstname character varying(20) NOT NULL,
    lastname character varying(20) NOT NULL,
    gender character(1) NOT NULL,
    superpower character varying(25) NOT NULL,
    dob date NOT NULL,
    iscurrentlyenrolled boolean NOT NULL,
    adminid integer NOT NULL
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Name: student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_id_seq OWNER TO postgres;

--
-- Name: student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_id_seq OWNED BY public.student.id;


--
-- Name: student_notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_notes (
    studentid integer NOT NULL,
    noteid integer NOT NULL
);


ALTER TABLE public.student_notes OWNER TO postgres;

--
-- Name: transcript; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transcript (
    classid integer NOT NULL,
    finalgrade double precision,
    studentid integer NOT NULL
);


ALTER TABLE public.transcript OWNER TO postgres;

--
-- Name: administrator id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrator ALTER COLUMN id SET DEFAULT nextval('public.administrator_id_seq'::regclass);


--
-- Name: classroom id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.classroom ALTER COLUMN id SET DEFAULT nextval('public.classroom_id_seq'::regclass);


--
-- Name: course_info id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_info ALTER COLUMN id SET DEFAULT nextval('public.course_info_id_seq'::regclass);


--
-- Name: note id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note ALTER COLUMN id SET DEFAULT nextval('public.note_id_seq'::regclass);


--
-- Name: student id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN id SET DEFAULT nextval('public.student_id_seq'::regclass);


--
-- Data for Name: administrator; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administrator (id, username, password) FROM stdin;
\.


--
-- Data for Name: class_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.class_type (type, name) FROM stdin;
\.


--
-- Data for Name: classroom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.classroom (id, building, roomnumber, capacity) FROM stdin;
\.


--
-- Data for Name: course_catalog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.course_catalog (sln, name, coursecredits, type) FROM stdin;
\.


--
-- Data for Name: course_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.course_info (id, sln, section, roomid, instructorname, "time", quarter, year) FROM stdin;
\.


--
-- Data for Name: note; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.note (id, note, date, type, adminid) FROM stdin;
\.


--
-- Data for Name: note_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.note_type (type, name) FROM stdin;
\.


--
-- Data for Name: quarter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quarter (type, name) FROM stdin;
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (id, firstname, lastname, gender, superpower, dob, iscurrentlyenrolled, adminid) FROM stdin;
\.


--
-- Data for Name: student_notes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student_notes (studentid, noteid) FROM stdin;
\.


--
-- Data for Name: transcript; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transcript (classid, finalgrade, studentid) FROM stdin;
\.


--
-- Name: administrator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administrator_id_seq', 1, false);


--
-- Name: classroom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.classroom_id_seq', 1, false);


--
-- Name: course_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.course_info_id_seq', 1, false);


--
-- Name: note_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.note_id_seq', 1, false);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_id_seq', 1, false);


--
-- Name: administrator administrator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrator
    ADD CONSTRAINT administrator_pkey PRIMARY KEY (id);


--
-- Name: class_type class_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_type
    ADD CONSTRAINT class_type_pkey PRIMARY KEY (type);


--
-- Name: classroom classroom_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.classroom
    ADD CONSTRAINT classroom_pkey PRIMARY KEY (id);


--
-- Name: course_catalog course_catalog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_catalog
    ADD CONSTRAINT course_catalog_pkey PRIMARY KEY (sln);


--
-- Name: course_info course_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_info
    ADD CONSTRAINT course_info_pkey PRIMARY KEY (id);


--
-- Name: note note_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note
    ADD CONSTRAINT note_pkey PRIMARY KEY (id);


--
-- Name: note_type note_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_type
    ADD CONSTRAINT note_type_pkey PRIMARY KEY (type);


--
-- Name: quarter quarter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quarter
    ADD CONSTRAINT quarter_pkey PRIMARY KEY (type);


--
-- Name: student student_adminid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_adminid_key UNIQUE (adminid);


--
-- Name: student_notes student_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_notes
    ADD CONSTRAINT student_notes_pkey PRIMARY KEY (studentid, noteid);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (id);


--
-- Name: transcript transcript_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transcript
    ADD CONSTRAINT transcript_pkey PRIMARY KEY (classid, studentid);


--
-- Name: course_catalog course_catalog_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_catalog
    ADD CONSTRAINT course_catalog_type_fkey FOREIGN KEY (type) REFERENCES public.class_type(type);


--
-- Name: course_info course_info_quarter_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_info
    ADD CONSTRAINT course_info_quarter_fkey FOREIGN KEY (quarter) REFERENCES public.quarter(type) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: course_info course_info_roomid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_info
    ADD CONSTRAINT course_info_roomid_fkey FOREIGN KEY (roomid) REFERENCES public.classroom(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: course_info course_info_sln_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_info
    ADD CONSTRAINT course_info_sln_fkey FOREIGN KEY (sln) REFERENCES public.course_catalog(sln) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: note note_adminid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note
    ADD CONSTRAINT note_adminid_fkey FOREIGN KEY (adminid) REFERENCES public.administrator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: note note_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note
    ADD CONSTRAINT note_type_fkey FOREIGN KEY (type) REFERENCES public.note_type(type) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: student student_adminid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_adminid_fkey FOREIGN KEY (adminid) REFERENCES public.administrator(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: student_notes student_notes_noteid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_notes
    ADD CONSTRAINT student_notes_noteid_fkey FOREIGN KEY (noteid) REFERENCES public.note(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: student_notes student_notes_studentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_notes
    ADD CONSTRAINT student_notes_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transcript transcript_classid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transcript
    ADD CONSTRAINT transcript_classid_fkey FOREIGN KEY (classid) REFERENCES public.course_info(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transcript transcript_studentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transcript
    ADD CONSTRAINT transcript_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

