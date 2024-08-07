PGDMP  4                    |           AppJo    16.1    16.1     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    33193    AppJo    DATABASE     z   CREATE DATABASE "AppJo" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE "AppJo";
                postgres    false            �            1259    33219    commande    TABLE     �  CREATE TABLE public.commande (
    id integer NOT NULL,
    id_utilisateurs integer NOT NULL,
    id_offre integer NOT NULL,
    nombre_ticket integer NOT NULL,
    statut_commande character varying(50) NOT NULL,
    date_commande timestamp with time zone NOT NULL,
    montant numeric(2,0) NOT NULL,
    methode_paiement character varying(50) NOT NULL,
    date_paiement timestamp with time zone NOT NULL,
    clef_transaction character varying(250) NOT NULL
);
    DROP TABLE public.commande;
       public         heap    postgres    false            �            1259    33218    commande_id_seq    SEQUENCE     �   CREATE SEQUENCE public.commande_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.commande_id_seq;
       public          postgres    false    220            �           0    0    commande_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.commande_id_seq OWNED BY public.commande.id;
          public          postgres    false    219            �            1259    33210    offre    TABLE     �   CREATE TABLE public.offre (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    nombre_personne integer NOT NULL,
    prix numeric(2,0) NOT NULL,
    description text NOT NULL
);
    DROP TABLE public.offre;
       public         heap    postgres    false            �            1259    33209    offre_id_seq    SEQUENCE     �   CREATE SEQUENCE public.offre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.offre_id_seq;
       public          postgres    false    218            �           0    0    offre_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.offre_id_seq OWNED BY public.offre.id;
          public          postgres    false    217            �            1259    33200    utilisateurs    TABLE     �  CREATE TABLE public.utilisateurs (
    id integer NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    hashed_password character varying(256) NOT NULL,
    clef_compte character varying(250) NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    salt character varying(100) NOT NULL
);
     DROP TABLE public.utilisateurs;
       public         heap    postgres    false            �            1259    33199    utilisateurs_id_seq    SEQUENCE     �   CREATE SEQUENCE public.utilisateurs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.utilisateurs_id_seq;
       public          postgres    false    216            �           0    0    utilisateurs_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.utilisateurs_id_seq OWNED BY public.utilisateurs.id;
          public          postgres    false    215            '           2604    33240    commande id    DEFAULT     j   ALTER TABLE ONLY public.commande ALTER COLUMN id SET DEFAULT nextval('public.commande_id_seq'::regclass);
 :   ALTER TABLE public.commande ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    219    220            &           2604    33241    offre id    DEFAULT     d   ALTER TABLE ONLY public.offre ALTER COLUMN id SET DEFAULT nextval('public.offre_id_seq'::regclass);
 7   ALTER TABLE public.offre ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218            $           2604    33242    utilisateurs id    DEFAULT     r   ALTER TABLE ONLY public.utilisateurs ALTER COLUMN id SET DEFAULT nextval('public.utilisateurs_id_seq'::regclass);
 >   ALTER TABLE public.utilisateurs ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216            �          0    33219    commande 
   TABLE DATA           �   COPY public.commande (id, id_utilisateurs, id_offre, nombre_ticket, statut_commande, date_commande, montant, methode_paiement, date_paiement, clef_transaction) FROM stdin;
    public          postgres    false    220   d        �          0    33210    offre 
   TABLE DATA           M   COPY public.offre (id, type, nombre_personne, prix, description) FROM stdin;
    public          postgres    false    218   �        �          0    33200    utilisateurs 
   TABLE DATA           t   COPY public.utilisateurs (id, firstname, lastname, email, hashed_password, clef_compte, is_admin, salt) FROM stdin;
    public          postgres    false    216   �        �           0    0    commande_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.commande_id_seq', 1, false);
          public          postgres    false    219            �           0    0    offre_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.offre_id_seq', 1, false);
          public          postgres    false    217            �           0    0    utilisateurs_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.utilisateurs_id_seq', 16, true);
          public          postgres    false    215            /           2606    33224    commande commande_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.commande
    ADD CONSTRAINT commande_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.commande DROP CONSTRAINT commande_pkey;
       public            postgres    false    220            -           2606    33217    offre offre_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.offre
    ADD CONSTRAINT offre_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.offre DROP CONSTRAINT offre_pkey;
       public            postgres    false    218            )           2606    33239    utilisateurs unique_email 
   CONSTRAINT     U   ALTER TABLE ONLY public.utilisateurs
    ADD CONSTRAINT unique_email UNIQUE (email);
 C   ALTER TABLE ONLY public.utilisateurs DROP CONSTRAINT unique_email;
       public            postgres    false    216            +           2606    33208    utilisateurs utilisateurs_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.utilisateurs
    ADD CONSTRAINT utilisateurs_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.utilisateurs DROP CONSTRAINT utilisateurs_pkey;
       public            postgres    false    216            0           2606    33230    commande offre    FK CONSTRAINT     n   ALTER TABLE ONLY public.commande
    ADD CONSTRAINT offre FOREIGN KEY (id_offre) REFERENCES public.offre(id);
 8   ALTER TABLE ONLY public.commande DROP CONSTRAINT offre;
       public          postgres    false    218    220    4653            1           2606    33225    commande utilisateurs    FK CONSTRAINT     �   ALTER TABLE ONLY public.commande
    ADD CONSTRAINT utilisateurs FOREIGN KEY (id_utilisateurs) REFERENCES public.utilisateurs(id);
 ?   ALTER TABLE ONLY public.commande DROP CONSTRAINT utilisateurs;
       public          postgres    false    220    216    4651            �      x������ � �      �      x������ � �      �      x������ � �     