from transformers import pipeline
import torch
import gradio as gr
import pandas as pd
transly = pipeline("translation", model="facebook/nllb-200-distilled-600M",torch_dtype=torch.bfloat16)
texty = pipeline("summarization", model="Falconsai/text_summarization",torch_dtype=torch.bfloat16)


lang_map = {
    "ace_Arab": "Acehnese",
    "ace_Latn": "Acehnese",
    "acm_Arab": "Mesopotamian Arabic",
    "acq_Arab": "Ta'izzi-Adeni Arabic",
    "aeb_Arab": "Tunisian Arabic",
    "afr_Latn": "Afrikaans",
    "ajp_Arab": "South Levantine Arabic",
    "aka_Latn": "Akan",
    "als_Latn": "Tosk Albanian",
    "amh_Ethi": "Amharic",
    "apc_Arab": "North Levantine Arabic",
    "arb_Arab": "Modern Standard Arabic",
    "arb_Latn": "Modern Standard Arabic",
    "ars_Arab": "Najdi Arabic",
    "ary_Arab": "Moroccan Arabic",
    "arz_Arab": "Egyptian Arabic",
    "asm_Beng": "Assamese",
    "ast_Latn": "Asturian",
    "awa_Deva": "Awadhi",
    "ayr_Latn": "Central Aymara",
    "azb_Arab": "South Azerbaijani",
    "azj_Latn": "North Azerbaijani",
    "bak_Cyrl": "Bashkir",
    "bam_Latn": "Bambara",
    "ban_Latn": "Balinese",
    "bel_Cyrl": "Belarusian",
    "bem_Latn": "Bemba",
    "ben_Beng": "Bengali",
    "bho_Deva": "Bhojpuri",
    "bjn_Arab": "Banjar Arabic",
    "bjn_Latn": "Banjar Latin",
    "bod_Tibt": "Tibetan",
    "bos_Latn": "Bosnian",
    "bug_Latn": "Buginese",
    "bul_Cyrl": "Bulgarian",
    "cat_Latn": "Catalan",
    "ceb_Latn": "Cebuano",
    "ces_Latn": "Czech",
    "cjk_Latn": "Chokwe",
    "ckb_Arab": "Central Kurdish",
    "crh_Latn": "Crimean Tatar",
    "cym_Latn": "Welsh",
    "dan_Latn": "Danish",
    "deu_Latn": "German",
    "dik_Latn": "Southwestern Dinka",
    "dyu_Latn": "Dyula",
    "dzo_Tibt": "Dzongkha",
    "ell_Grek": "Greek",
    "eng_Latn": "English",
    "epo_Latn": "Esperanto",
    "est_Latn": "Estonian",
    "eus_Latn": "Basque",
    "ewe_Latn": "Ewe",
    "fao_Latn": "Faroese",
    "fij_Latn": "Fijian",
    "fin_Latn": "Finnish",
    "fon_Latn": "Fon",
    "fra_Latn": "French",
    "fur_Latn": "Friulian",
    "fuv_Latn": "Nigerian Fulfulde",
    "gla_Latn": "Scottish Gaelic",
    "gle_Latn": "Irish",
    "glg_Latn": "Galician",
    "grn_Latn": "Guarani",
    "guj_Gujr": "Gujarati",
    "hat_Latn": "Haitian Creole",
    "hau_Latn": "Hausa",
    "heb_Hebr": "Hebrew",
    "hin_Deva": "Hindi",
    "hne_Deva": "Chhattisgarhi",
    "hrv_Latn": "Croatian",
    "hun_Latn": "Hungarian",
    "hye_Armn": "Armenian",
    "ibo_Latn": "Igbo",
    "ilo_Latn": "Ilocano",
    "ind_Latn": "Indonesian",
    "isl_Latn": "Icelandic",
    "ita_Latn": "Italian",
    "jav_Latn": "Javanese",
    "jpn_Jpan": "Japanese",
    "kab_Latn": "Kabyle",
    "kac_Latn": "Jingpho",
    "kam_Latn": "Kamba",
    "kan_Knda": "Kannada",
    "kas_Arab": "Kashmiri (Arabic)",
    "kas_Deva": "Kashmiri (Devanagari)",
    "kat_Geor": "Georgian",
    "knc_Arab": "Kanuri (Arabic)",
    "knc_Latn": "Kanuri (Latin)",
    "kaz_Cyrl": "Kazakh",
    "kbp_Latn": "Kabiyè",
    "kea_Latn": "Kabuverdianu",
    "khm_Khmr": "Khmer",
    "kik_Latn": "Kikuyu",
    "kin_Latn": "Kinyarwanda",
    "kir_Cyrl": "Kyrgyz",
    "kmb_Latn": "Kimbundu",
    "kmr_Latn": "Kurmanji Kurdish",
    "kon_Latn": "Kikongo",
    "kor_Hang": "Korean",
    "lao_Laoo": "Lao",
    "lij_Latn": "Ligurian",
    "lim_Latn": "Limburgish",
    "lin_Latn": "Lingala",
    "lit_Latn": "Lithuanian",
    "lmo_Latn": "Lombard",
    "ltg_Latn": "Latgalian",
    "ltz_Latn": "Luxembourgish",
    "lua_Latn": "Luba-Kasai",
    "lug_Latn": "Ganda",
    "luo_Latn": "Luo",
    "lus_Latn": "Mizo",
    "lvs_Latn": "Latvian",
    "mag_Deva": "Magahi",
    "mai_Deva": "Maithili",
    "mal_Mlym": "Malayalam",
    "mar_Deva": "Marathi",
    "min_Latn": "Minangkabau",
    "mkd_Cyrl": "Macedonian",
    "mlt_Latn": "Maltese",
    "mfe_Latn": "Mauritian Creole",
    "mon_Cyrl": "Mongolian",
    "mos_Latn": "Mossi",
    "mri_Latn": "Maori",
    "msa_Latn": "Malay",
    "mya_Mymr": "Burmese",
    "nld_Latn": "Dutch",
    "nno_Latn": "Norwegian Nynorsk",
    "nob_Latn": "Norwegian Bokmål",
    "npi_Deva": "Nepali",
    "nso_Latn": "Northern Sotho",
    "nus_Latn": "Nuer",
    "nya_Latn": "Chichewa",
    "oci_Latn": "Occitan",
    "ory_Orya": "Odia",
    "pag_Latn": "Pangasinan",
    "pan_Guru": "Punjabi (Gurmukhi)",
    "pap_Latn": "Papiamento",
    "pbt_Arab": "Pashto (Southern)",
    "pes_Arab": "Persian (Farsi)",
    "plt_Latn": "Plateau Malagasy",
    "pol_Latn": "Polish",
    "por_Latn": "Portuguese",
    "prs_Arab": "Dari Persian",
    "quy_Latn": "Quechua",
    "ron_Latn": "Romanian",
    "run_Latn": "Rundi",
    "rus_Cyrl": "Russian",
    "sag_Latn": "Sango",
    "san_Deva": "Sanskrit",
    "sat_Olck": "Santali (Ol Chiki)",
    "scn_Latn": "Sicilian",
    "shn_Mymr": "Shan",
    "sin_Sinh": "Sinhala",
    "slk_Latn": "Slovak",
    "slv_Latn": "Slovenian",
    "smo_Latn": "Samoan",
    "sna_Latn": "Shona",
    "snd_Arab": "Sindhi",
    "som_Latn": "Somali",
    "sot_Latn": "Southern Sotho",
    "spa_Latn": "Spanish",
    "srd_Latn": "Sardinian",
    "srp_Cyrl": "Serbian",
    "ssw_Latn": "Swati",
    "sun_Latn": "Sundanese",
    "swe_Latn": "Swedish",
    "swh_Latn": "Swahili",
    "szl_Latn": "Silesian",
    "tam_Taml": "Tamil",
    "tat_Cyrl": "Tatar",
    "tel_Telu": "Telugu",
    "tgk_Cyrl": "Tajik",
    "tgl_Latn": "Tagalog",
    "tha_Thai": "Thai",
    "tir_Ethi": "Tigrinya",
    "tpi_Latn": "Tok Pisin",
    "tsn_Latn": "Tswana",
    "tso_Latn": "Tsonga",
    "tuk_Latn": "Turkmen",
    "tum_Latn": "Tumbuka",
    "tur_Latn": "Turkish",
    "twi_Latn": "Twi",
    "tzm_Tfng": "Central Atlas Tamazight",
    "uig_Arab": "Uyghur",
    "ukr_Cyrl": "Ukrainian",
    "umb_Latn": "Umbundu",
    "urd_Arab": "Urdu",
    "uzn_Latn": "Uzbek",
    "vec_Latn": "Venetian",
    "vie_Latn": "Vietnamese",
    "war_Latn": "Waray",
    "wol_Latn": "Wolof",
    "xho_Latn": "Xhosa",
    "ydd_Hebr": "Yiddish",
    "yor_Latn": "Yoruba",
    "yue_Hant": "Cantonese (Traditional Chinese)",
    "zho_Hans": "Chinese (Simplified)",
    "zho_Hant": "Chinese (Traditional)",
    "zsm_Latn": "Malay (Latin)",
    "zul_Latn": "Zulu"
}

df = pd.DataFrame(list(lang_map.items()), columns=["Code", "Language"])
def summarize_text(text):
    return texty(
        text,
        max_length=60,
        min_length=15,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.8,
        num_beams=4
    )[0]['summary_text']


def MultiTranslator(text, src_lang, tgt_lang):
    # Get codes
    Source = df.loc[df['Language'] == src_lang, 'Code'].values[0]
    Target = df.loc[df['Language'] == tgt_lang, 'Code'].values[0]


    result = transly(text, src_lang=Source, tgt_lang=Target)
    translated_text = result[0]['translation_text']


    if len(text.split()) < 5:
        summary = f"Input too short for summarization in {tgt_lang}."
    else:

        if tgt_lang == "English":
            summary = summarize_text(translated_text)
        else:

            text_in_english = transly(text, src_lang=Source, tgt_lang="eng_Latn")[0]['translation_text']
            summary_en = summarize_text(text_in_english)
            summary_tgt = transly(summary_en,src_lang="eng_Latn", tgt_lang=Target)[0]['translation_text']
            summary = summary_tgt

    return (
        f"**Translation**\n\n{tgt_lang}: {translated_text}",
        f"**Summary in {tgt_lang}:**\n\n{summary}"
    )

with gr.Blocks() as grad:
    gr.Markdown(" 🌍 Multi-Language Translator + Summarizer")

    with gr.Row():
        text_input = gr.Textbox(label="Enter text", placeholder="Type your text here...", lines=3)

    with gr.Row():
        src_lang = gr.Dropdown(choices=df["Language"].tolist(), label="Source Language", value="English")
        tgt_lang = gr.Dropdown(choices=df["Language"].tolist(), label="Target Language", value="Hindi")
    with gr.Row():
        translate_output = gr.Textbox(label="Translated Text", lines=5)
        summary_output = gr.Textbox(label="Summary", lines=5)

    submit_btn = gr.Button("Translate & Summarize")

    submit_btn.click(
        MultiTranslator,
        inputs=[text_input, src_lang, tgt_lang],
        outputs=[translate_output, summary_output]
    )

grad.launch()



