PGDMP      
                |           appjo    16.2    16.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                        0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    17000    appjo    DATABASE     x   CREATE DATABASE appjo WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE appjo;
                postgres    false            �            1259    17001    commande    TABLE     �  CREATE TABLE public.commande (
    id integer NOT NULL,
    user_id integer NOT NULL,
    offer_id integer NOT NULL,
    ticket_number integer NOT NULL,
    order_status character varying(50) NOT NULL,
    order_date timestamp with time zone NOT NULL,
    amount numeric(10,2) NOT NULL,
    payment_method character varying(50) NOT NULL,
    payment_date timestamp with time zone NOT NULL,
    transaction_key character varying(250) NOT NULL
);
    DROP TABLE public.commande;
       public         heap    postgres    false            �            1259    17004    commande_id_seq    SEQUENCE     �   CREATE SEQUENCE public.commande_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.commande_id_seq;
       public          postgres    false    215                       0    0    commande_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.commande_id_seq OWNED BY public.commande.id;
          public          postgres    false    216            �            1259    17005    offre    TABLE     �   CREATE TABLE public.offre (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    nombre_personne integer NOT NULL,
    prix numeric(7,2) NOT NULL,
    description text NOT NULL,
    image character varying(255)
);
    DROP TABLE public.offre;
       public         heap    postgres    false            �            1259    17010    offre_id_seq    SEQUENCE     �   CREATE SEQUENCE public.offre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.offre_id_seq;
       public          postgres    false    217                       0    0    offre_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.offre_id_seq OWNED BY public.offre.id;
          public          postgres    false    218            �            1259    17011    utilisateurs    TABLE     �  CREATE TABLE public.utilisateurs (
    user_id integer NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    hashed_password character varying(256) NOT NULL,
    account_key character varying(250) NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    salt character varying(100) NOT NULL
);
     DROP TABLE public.utilisateurs;
       public         heap    postgres    false            �            1259    17017    utilisateurs_id_seq    SEQUENCE     �   CREATE SEQUENCE public.utilisateurs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.utilisateurs_id_seq;
       public          postgres    false    219                       0    0    utilisateurs_id_seq    SEQUENCE OWNED BY     P   ALTER SEQUENCE public.utilisateurs_id_seq OWNED BY public.utilisateurs.user_id;
          public          postgres    false    220            Z           2604    17018    commande id    DEFAULT     j   ALTER TABLE ONLY public.commande ALTER COLUMN id SET DEFAULT nextval('public.commande_id_seq'::regclass);
 :   ALTER TABLE public.commande ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215            [           2604    17019    offre id    DEFAULT     d   ALTER TABLE ONLY public.offre ALTER COLUMN id SET DEFAULT nextval('public.offre_id_seq'::regclass);
 7   ALTER TABLE public.offre ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217            \           2604    17020    utilisateurs user_id    DEFAULT     w   ALTER TABLE ONLY public.utilisateurs ALTER COLUMN user_id SET DEFAULT nextval('public.utilisateurs_id_seq'::regclass);
 C   ALTER TABLE public.utilisateurs ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    220    219            �          0    17001    commande 
   TABLE DATA           �   COPY public.commande (id, user_id, offer_id, ticket_number, order_status, order_date, amount, payment_method, payment_date, transaction_key) FROM stdin;
    public          postgres    false    215   �        �          0    17005    offre 
   TABLE DATA           T   COPY public.offre (id, type, nombre_personne, prix, description, image) FROM stdin;
    public          postgres    false    217   �        �          0    17011    utilisateurs 
   TABLE DATA           y   COPY public.utilisateurs (user_id, firstname, lastname, email, hashed_password, account_key, is_admin, salt) FROM stdin;
    public          postgres    false    219   �!                  0    0    commande_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.commande_id_seq', 10, true);
          public          postgres    false    216                       0    0    offre_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.offre_id_seq', 5, true);
          public          postgres    false    218                       0    0    utilisateurs_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.utilisateurs_id_seq', 6, true);
          public          postgres    false    220            _           2606    17024    offre offre_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.offre
    ADD CONSTRAINT offre_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.offre DROP CONSTRAINT offre_pkey;
       public            postgres    false    217            a           2606    17026    utilisateurs unique_email 
   CONSTRAINT     U   ALTER TABLE ONLY public.utilisateurs
    ADD CONSTRAINT unique_email UNIQUE (email);
 C   ALTER TABLE ONLY public.utilisateurs DROP CONSTRAINT unique_email;
       public            postgres    false    219            c           2606    17028    utilisateurs utilisateurs_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.utilisateurs
    ADD CONSTRAINT utilisateurs_pkey PRIMARY KEY (user_id);
 H   ALTER TABLE ONLY public.utilisateurs DROP CONSTRAINT utilisateurs_pkey;
       public            postgres    false    219            d           2606    17054    commande commande_pkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.commande
    ADD CONSTRAINT commande_pkey FOREIGN KEY (offer_id) REFERENCES public.offre(id) ON DELETE SET NULL;
 @   ALTER TABLE ONLY public.commande DROP CONSTRAINT commande_pkey;
       public          postgres    false    215    217    4703            e           2606    17029    commande offre    FK CONSTRAINT     n   ALTER TABLE ONLY public.commande
    ADD CONSTRAINT offre FOREIGN KEY (offer_id) REFERENCES public.offre(id);
 8   ALTER TABLE ONLY public.commande DROP CONSTRAINT offre;
       public          postgres    false    217    215    4703            f           2606    17034    commande utilisateurs    FK CONSTRAINT     �   ALTER TABLE ONLY public.commande
    ADD CONSTRAINT utilisateurs FOREIGN KEY (user_id) REFERENCES public.utilisateurs(user_id);
 ?   ALTER TABLE ONLY public.commande DROP CONSTRAINT utilisateurs;
       public          postgres    false    4707    215    219            �      x������ � �      �   �   x���1�0��9��nQ[@bF����ԠHm�8+���h��Z�Y_��ag��"v�Pö�e����+�XsB��#y�#�Z
)���H8�M�8��'����[��j�Z��K3����͛4��؟�!!��2�g�`�Ȋ�� ⹠1zv�����d%���RZA��      �   [  x�MϻR�0��Z~F�ѵ�d�ـIb�1��F>�q.�B�$O3�|����]���/X��f��e?����K$�t*
�h���v�!)�G$B�%7��2ZaJ����4�����\<�8�k��e����}Ks�ץ���!���̚��|��O�P͖�z���i��Ԧ��Q�#���G#�T�@ �H�����a��8���-y'��ס�A+/9����"b�	��p�:.j�n��,���"�#�jU�jqY���Z�_���e���A���m8�0��z|Ynm�uو��dڴ�]��5�I���1n�O��萴� ��P���Cٿ�,�>�B�>     