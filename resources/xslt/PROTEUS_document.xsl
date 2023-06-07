<!-- PROTEUS_document.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:proteus="http://proteus.lsi.us.es">
    <!-- Match the root object of the document -->
    <xsl:template match="proteus:object[@classes=':Proteus-document']">
        <html>
            <head>
                <title>
                    <!-- Display the name property as the document title -->
                    <xsl:value-of select="proteus:properties/proteus:stringProperty[@name='name']"/>
                </title>
                <style>
                    /* Add custom styles for the document */
                    body {
                        font-family: Arial, sans-serif;
                    }
                    h1 {
                        font-size: 24px;
                        font-weight: bold;
                        text-align: center;
                    }
                    h2 {
                        font-size: 16px;
                        font-weight: normal;
                    }
                    table {
                        margin: 20px auto;
                        border-collapse: collapse;
                    }
                    td {
                        padding: 5px 10px;
                    }
                    ul {
                        list-style-type: none;
                        padding-left: 0;
                    }
                    .indent {
                        margin-left: 20px;
                    }
                </style>
            </head>
            <body>
                <!-- Render the front page -->
                <div>
                    <h1>
                        <!-- Display the document name centered in big and bold font -->
                        <xsl:value-of select="proteus:properties/proteus:stringProperty[@name='name']"/>
                    </h1>
                    <h2>
                        <!-- Display the author name in smaller and non-bold font -->
                        <xsl:value-of select="proteus:properties/proteus:stringProperty[@name='author']"/>
                    </h2>
                    <p style="text-align: right;">
                        <!-- Display the creation date in the document's right corner -->
                        <xsl:value-of select="proteus:properties/proteus:dateProperty[@name='date']"/>
                    </p>
                </div>
                <!-- Render the index for children -->
                <div>
                    <h1>Index</h1>
                    <ul>
                        <!-- Render the index for children objects -->
                        <xsl:apply-templates select="proteus:children/proteus:object"/>
                    </ul>
                </div>
            </body>
        </html>
    </xsl:template>

    <!-- Match any property -->
    <xsl:template match="proteus:properties/*">
        <tr>
            <td>
                <xsl:value-of select="@name"/>
            </td>
            <td>
                <xsl:value-of select="."/>
            </td>
        </tr>
    </xsl:template>
    
    <!-- Match section objects -->
    <xsl:template match="proteus:object[@classes='section']">
        <li>
            <!-- Display the section name -->
            <xsl:value-of select="proteus:properties/proteus:stringProperty[@name='name']"/>
            <!-- Render the index for children objects of the section -->
            <ul class="indent">
                <xsl:apply-templates select="proteus:children/proteus:object"/>
            </ul>
        </li>
    </xsl:template>
    
    <!-- Match paragraph objects -->
    <xsl:template match="proteus:object[@classes='paragraph']">
        <p>
            <!-- Display the paragraph name -->
            <xsl:value-of select="proteus:properties/proteus:stringProperty[@name='name']"/>
        </p>
    </xsl:template>
</xsl:stylesheet>
