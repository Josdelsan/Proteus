<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_main.xsl                               -->
<!-- Content : PROTEUS default XSLT main file                 -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/06/09                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->
<!-- Update  : 2024/09/08 (Amador Durán)                      -->
<!-- encoding="iso-8859-1" -> enconding="utf-8"               -->
<!-- graphica_file -> local_resource                          -->
<!-- external_resource -> remote_resource                     -->
<!-- archetype_link -> symbolic_link                          -->
<!-- ======================================================== -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>
    <!-- Output -->
    <xsl:output method="html"
        doctype-public="XSLT-compat"
        omit-xml-declaration="yes"
        encoding="utf-8"
        indent="yes"
    />

    <!-- Template includes -->
    <xsl:include href="PROTEUS_utilities.xsl" />
    <xsl:include href="PROTEUS_properties.xsl" />
    <xsl:include href="PROTEUS_cover.xsl" />
    <xsl:include href="PROTEUS_document.xsl" />

    <xsl:include href="archetypes/general/section.xsl" />
    <xsl:include href="archetypes/general/appendix.xsl" />
    <xsl:include href="archetypes/general/paragraph.xsl" />
    <xsl:include href="archetypes/general/glossary_item.xsl" />
    <xsl:include href="archetypes/general/figure.xsl" />
    <xsl:include href="archetypes/general/organization.xsl" />
    <xsl:include href="archetypes/general/stakeholder.xsl" />
    <xsl:include href="archetypes/general/meeting.xsl" />
    <xsl:include href="archetypes/general/symbolic_link.xsl" />

    <xsl:include href="archetypes/madeja/strength.xsl" />
    <xsl:include href="archetypes/madeja/weakness.xsl" />
    <xsl:include href="archetypes/madeja/PROTEUS_user_story.xsl" />

    <xsl:include href="archetypes/software/PROTEUS_actor.xsl" />
    <xsl:include href="archetypes/PROTEUS_default.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_information_requirement.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_objective.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_use_case.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_constraint.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_functional_requirement.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_nonfunctional_requirement.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_object_type.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_association_type.xsl" />
    <xsl:include href="archetypes/software/PROTEUS_traceability_matrix.xsl" />
    <xsl:include href="archetypes/madeja/PROTEUS_business_actor.xsl" />
    <xsl:include href="archetypes/madeja/PROTEUS_business_process.xsl" />

    <xsl:template match="project">
        <xsl:variable name="currentDocumentId" select="proteus-utils:current_document()"/>
        <xsl:for-each select="documents">
            <xsl:if test="object[@id=$currentDocumentId]">
                <xsl:apply-templates select="object[@id=$currentDocumentId]"/>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>