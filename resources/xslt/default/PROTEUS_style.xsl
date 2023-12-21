<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_style.xsl                              -->
<!-- Content : PROTEUS XSLT for template style                -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/08/10                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<!-- This is not being used. It is an inefficient alternative -->
<!-- to allow styles when there is no internet connection.    -->

<!-- Style tags have a mb limit so all styles are not loaded. -->

<!-- Using standart css files was tried but did not work due  -->
<!-- to PyQt QWebEnginePage local/external resources conflict -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>
    
    <!-- ============================================= -->
    <!-- proteus style                                 -->
    <!-- ============================================= -->
    <xsl:template name="style">

        <style>
            <!-- ================= -->
            <!-- Printing          -->
            <!-- ================= -->
            @media print {
                .page-break {
                  clear: both;
                  page-break-before: always;
                }
              }

              table {
                width: 98%;
                margin: 0 auto;
                margin-bottom: 2em;
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
            }

            <!-- ================= -->
            <!-- General style     -->
            <!-- ================= -->

            body {
            font-family: calibri,cambria,verdana,arial;
            font-size:   12pt;
            text-align:  justify;
            }

            body > div {
            margin-top: 1em;
            margin-bottom: 1.5em;
            }

            span.tbd {
            color: red;
            font-weight: bold;
            }

            code {
            font-size: small;
            }

            textarea.markdown {
            display: none;
            }

            <!-- Warnings -->

            div#warning_container {
            display: none;
            padding: 6px;
            margin-bottom: 10pt;
            font-size: small;
            background-color: lightyellow;
            }

            span#warning_title {
            font-weight: bold;
            }

            div#warning_messages ul {
            margin-top: 6px;
            margin-bottom: 6px;
            }

            <!-- Document cover -->

            div#document_cover {
            text-align: center;
            }

            <!-- Debugging -->
            div#browser_info {
            display: none;
            }

            div#project_name,
            div#document_version,
            div#document_date {
            font-weight: bold;
            font-size: large;
            }

            div#project_name {
            margin-bottom: 50pt;
            }

            div#document_logo {
            margin-bottom: 20pt;
            }

            div#document_name {
            font-weight: bold;
            font-size: xx-large;
            margin-bottom: 20pt;
            }

            div#document_version {
            margin-bottom: 20pt;
            }

            div#document_date {
            margin-bottom: 50pt;
            }

            div#document_prepared_by {
            margin-bottom: 100pt;
            }

            <!-- Table of content -->

            ul.toc_list {
            list-style-type: none;
            list-style-position: outside;
            list-style-image: none;
            line-height: 150%;
            font-weight: normal;
            }

            ul.toc_list_level_1 {
            margin-left: 0pt;
            font-weight: bold;
            }

            <!-- Parts -->

            div.part {
            font-size:   xx-large;
            font-weight: bold;
            text-align:  center;
            line-height: 150%;
            margin-top: 200pt;
            margin-bottom: 200pt;
            }

            <!-- Glossary items -->

            div.glo > span,
            div.bib > span {
            float: left;
            }

            div.glo p,
            div.bib p {
            padding-left: 2em;
            }

            div.glo p:first-child,
            div.bib p:first-child {
            text-indent: -2em;
            }

            div.glo > span.glo {
            font-weight: bold;
            }

            <!-- Info paragrahps -->

            div.info {
            margin-top: 16px;
            margin-bottom: 16px;
            padding: 8px;
            background-color: lightyellow;
            border: goldenrod solid;
            border-width: 1px;
            }

            <!-- TODO url using CDN like github -->
            div.info > div {
            background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAERUExURQAAAP/GOf/IN//ISf/MRP/MQv/GQP/NQP/KQP/KQP/JQf3LQf3LQf3KQf3MQf3KQP3LQf7LQP/LQf7KQP7KQv7KP/7KQf7KQf7KQf7LQP7KQP7LQP7KP/7KP/7KQf7LQf7KQf7LQf7KQP/LQf/LQv/LQ//MQ//MRf/MRv/NSP/OTP/OTf/PTv/QUv/QU//RVf/RV//RWf/SW//TXv/TX//WaP/XbP/Ycf/ad//fif/fi//gjv/gj//hkP/hkv/ilP/knP/knv/lnv/mo//npv/nqP/oqv/rtf/uwP/uwf/vw//wyf/xy//y0f/z1f/34v/45v/45//56f/67P/77//78P/88//99//++v/+/f///4M/5sUAAAAjdFJOUwAJDg4PIyQkMFdaiYqampucyszS0unp6uvs9PT1+fn5+vv8T/4+zAAAAAlwSFlzAAALEgAACxIB0t1+/AAAAW5JREFUOE91k+lWwjAQhVNESqGtlEUKIlqCG264b7grKu675v0fxGlyLck5+v26M3dOmkxn2JARxwvCqFUrFnJppHTssQme0PBHkf7Fcqfhgcm8BUuSKSOvUbZhEtkqkgbVLGyW+dOniozyLf38xcvBQRual9Q9XISSOyHEETTn+di39fu3v6ngBgG9JX6tj0BxSwU9aMKn/mn9ITrn13uQMY00cyD/Icc8KMXy6iwUKLAAiljvPwvxuotIUWQhFNE7vaIrvs8jlNRYBKV4oYoVaEnLLGh/CPE1h0AS6Z/gfJMOeIBWhPolOT+mgjNoRWA+M+7jFrTCMxq18CnE2wwChWO0eocOGEAr6injZ/Wo4AJaQT9L/937VHDfXesi5Lwp53I4MEtPVCEeNxBy7sa+PnKdw/7JNjSBkft3aCvJ9mTHkTKoJGNPZ5SQ1CgZ22e5U8iDpmusHmH7dXhE3df2LiEl1z8KA8+h/ikY+wFGwHtzSILYxAAAAABJRU5ErkJggg==');
            background-repeat: no-repeat;
            background-position: left top;
            min-height: 2em;
            padding-left: 42px;
            }

            <!-- Figures and traceability matrices with captions -->

            div.figure,
            div.traceability_matrix {
            text-align: center;
            }

            img.figure_image {

            }

            p.figure_caption,
            p.matrix_caption {
            margin-top: 4px;
            }

            span.figure_caption_label,
            span.matrix_caption_label {
            font-weight: bold;
            }

            <!-- old REMUS tables - general styles -->

            table.madeja_object > thead > tr
            {
            background-color: rgb(207, 243, 207);
            }

            table.remus_table {
            margin-left: 1%;
            margin-right: 1%;
            width: 98%;
            box-shadow: 8px 8px 4px lightgrey;
            }

            table.remus_table,
            table.remus_table th,
            table.remus_table td {
            border-style: solid;
            border-collapse: collapse;
            border-color: lightslategray;
            border-width: 1px;
            }

            table.remus_table th,
            table.remus_table td {
            padding: 8px;
            vertical-align: top;
            }

            table.remus_table th.name_column {
            width: 100%;
            }

            <!-- first row, first column -->
            table.remus_table > thead > tr > th:first-child {
            padding-left: 12px;
            padding-right: 12px;
            padding-bottom: 4px;
            min-width: 7.25em;
            }

            <!-- any row, first column -->
            table.remus_table tr > th:first-child {
            }

            <!-- icon on the first row, first column -->
            table.remus_table > thead > tr > th:first-child > img:first-child {
            padding-right: 0.25em;
            vertical-align: text-bottom;
            width: 18px;
            }

            <!-- paragraphs inside tables -->
            table.remus_table p {
            margin-top: 0em;
            margin-bottom: 0em;
            }

            table.remus_table div.remus_comments p {
            margin-top: 0em;
            margin-bottom: 0em;
            }

            <!-- lists inside tables -->
            table.remus_table td ul.stakeholders,
            table.remus_table td ul.subobjectives,
            table.remus_table td ul.specific_data,
            table.remus_table td ul.affected_objects {
            margin-top: 0em;
            margin-bottom: 0em;
            margin-left: 1em;
            padding-left: 0em;
            }

            <!-- general purpose objects -->

            table.organization > thead > tr,
            table.stakeholder  > thead > tr,
            table.meeting      > thead > tr
            {
            background-color: lightcyan;
            }

            <!-- requirements objects -->

            table.objective > thead > tr,
            table.actor > thead > tr,
            table.information_requirement > thead > tr,
            table.constraint_requirement > thead > tr,
            table.use_case > thead > tr,
            table.functional_requirement > thead > tr,
            table.nonfunctional_requirement > thead > tr
            {
            background-color: powderblue;
            }

            span.subobjective {
            font-weight: bold;
            }

            span.relevant_concept,
            span.triggering_event,
            span.exception_termination {
            font-style: italic;
            }

            <!-- use case tables -->

            table.use_case th.step_action_column,
            table.use_case th.exception_action_column {
            width: 100%;
            }

            table.use_case th.step_number_column {
            text-align: center;
            }

            table.use_case th.step_number {
            text-align: center;
            font-weight: normal;
            }

            <!-- traceability matrices -->

            table.traceability_matrix {
            margin-bottom: 1em;
            }

            table.traceability_matrix > thead > tr {
            background-color: lightgoldenrodyellow;
            }

            <!-- first row, first column -->
            table.traceability_matrix > thead > tr > th:first-child {
            width: 7.5em;
            }

            table.traceability_matrix th {
            padding-left: 0;
            padding-right: 0;
            }

            table.traceability_matrix button.reduce_font,
            table.traceability_matrix button.increase_font {
            height: 1.75em;
            color: black;
            border: 2px;
            padding-left: 4px;
            padding-right: 4px;
            padding-top: 1px;
            padding-bottom: 1px;
            margin-top: 4px;
            margin-left: 2px;
            margin-right: 2px;
            font-weight: bold;
            }

            <!-- TODO: url using CDN like github -->
            table.traceability_matrix td.trace {

            }

            <!-- modeling objects -->

            table.object_type > thead > tr,
            table.value_type > thead > tr,
            table.association_type > thead > tr,
            table.system_operation > thead > tr
            {
            background-color: gainsboro;
            }

            div.code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 11pt;
            }

            div.code_description, div.code_ocl {
            padding-left: 1.25em;
            }

            span.keyword {
            color: purple;
            font-weight: bold;
            }

            span.abstract {
            font-style: italic;
            }

            span.class_name {
            font-weight: bold;
            }

            div.code_comment, span.code_comment {
            color: darkgreen;
            font-style: italic;
            }

            div.code_header {
            padding-left: 1.5em;
            font-weight: bold;
            }

            ul.properties {
            margin-top: 0px;
            margin-bottom: 0px;
            margin-left: 1.5em;
            padding-left: 0px;
            }

            li.property {
            list-style: none;
            padding-left: 0px;
            margin-left: 0px;
            }

            <!-- management objects -->

            table.conflict > thead > tr,
            table.defect > thead > tr,
            table.change_request > thead > tr
            {
            background-color: pink;
            }

            <!-- information icon in defect table header -->
            table.defect > thead > tr th img.info_icon {
            vertical-align: text-bottom;
            width: 18px;
            }

            span.alternative_name {
            font-weight: bold;
            }

            table.remus_table td ol.alternatives {
            margin-top: 0em;
            margin-bottom: 0em;
            margin-left: 1.5em;
            padding-left: 0em;
            }

            table.remus_table td ol.alternatives li.alternative {
            margin-bottom: 1em;
            }

            .alternative_description {
            font-style: italic;
            }
        </style>

    </xsl:template>
    

</xsl:stylesheet>