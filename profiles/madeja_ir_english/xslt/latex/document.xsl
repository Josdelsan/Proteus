<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus"
>
    <!-- Match the root object of the document -->
    <xsl:template match="object[@classes=':Proteus-document']">

    <html>

    \documentclass[conference,a4paper]{IEEEtran}

    \begin{document}

    \title{<xsl:apply-templates select="properties/*[@name=':Proteus-name']"/>}

    \begin{abstract}
    <xsl:apply-templates select="properties/*[@name='description']"/>
    \end{abstract}

    <xsl:apply-templates select="children/object"/>

    \end{document}
    
    <script src="templates:///latex/script.js"></script>

    </html>

    </xsl:template>

</xsl:stylesheet>