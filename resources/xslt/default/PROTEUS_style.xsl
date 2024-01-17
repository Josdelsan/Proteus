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
            <!-- Printing -->
            @media print {
                .page-break {
                    clear: both;
                    page-break-before: always;
                }
            }

            <!-- Tables -->
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

            <!-- Symlinked objects -->
            .linked-object {
                background-color: #fcfce6;
                position: relative;
                cursor: pointer;
            }

        </style>

    </xsl:template>
    

</xsl:stylesheet>