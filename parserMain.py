from analisys.gradleParser import parserGradle
from analisys.mavenParser import parserMaven
from analisys.rubyParser import parserRuby
from domain.GradleLog import GradleLog
from domain.MavenLog import MavenLog
from parserGeneral import *
from parserGradle import *
from parserMaven import maven_parser
from parserRake import parserRake
from domain.RubyLog import RubyLog



#maven
# controllare Vanilla


#checkstyle project fa partire un Gradle demon all'interno di Maven... -.-''''

#problemi iniziali!
# reponame="apache/tajo"
# f = open('logs\\maven\\apache_tajo\\tajo-5965-166162229.txt', 'r')
# reponame="javaee-samples/javaee7-samples"
# f = open('logs\\maven\\javaee-samples_javaee7-samples\\javaee7-samples-243-177091125.txt', 'r')

#test error
# reponame="Mashape/unirest-java"
# f = open('logs\\maven\\Mashape_unirest-java\\unirest-java-455-173553449.txt', 'r')
# f = open('logs\\maven\\Mashape_unirest-java\\unirest-java-455-173553451.txt', 'r')

#errori di compilazione
# reponame="SpoutDev/Vanilla"
# f = open('logs\\maven\\SpoutDev_Vanilla\\Vanilla-178-7018610.txt', 'r')
# f = open('logs\\maven\\SpoutDev_Vanilla\\Vanilla-179-22527723.txt', 'r')
#errori di test
# reponame="springside/springside4"
# f = open('logs\\maven\\springside_springside4\\springside4-449-165962220.txt', 'r')


# #compilation error e errore di lettura file zip
# reponame="tinkerpop/gremlin"
# f = open('logs\\maven\\tinkerpop_gremlin\\gremlin-185-170106481.txt', 'r')

#errori di compilazione
# reponame="pulse00/Twig-Eclipse-Plugin"
# f = open('logs\\maven\\Twig-Eclipse-Plugin\\Twig-Eclipse-Plugin-137-168865827.txt', 'r')


#passed
# reponame="simpligility/android-maven-plugin"
# f = open('logs\\maven\\android-maven-plugin\\android-maven-plugin-1233-156907093.txt', 'r')


#errori di test
# reponame="jhy/jsoup"
# f = open('logs\\maven\\jsoup\\jsoup-406-176552717.txt', 'r')

#passed
# reponame="JodaOrg/joda-time"
# f = open('logs\\maven\\JodaOrg_joda-time\\joda-time-415-175370840.txt', 'r')

#passed, fa solo test
# reponame="bitcoinj/bitcoinj"
# f = open('logs\\maven\\bitcoinj_bitcoinj\\bitcoinj-1844-174824456.txt', 'r')

# #errori di test
# reponame="languagetool-org/languagetool"
# # f = open('logs\\maven\\languagetool-org_languagetool\\languagetool-4133-177081242.txt', 'r')
# f = open('logs\\maven\\languagetool-org_languagetool\\languagetool-4487-186715344.txt', 'r')


#status passed
# reponame="google/error-prone"
# f = open('logs\\maven\\google_error-prone\\error-prone-523-174617444.txt', 'r')

#errore dipendenze
# reponame="spotify/helios"
# f = open('logs\\maven\\spotify_helios\\helios-784-25695663.txt', 'r')

#passed
# reponame="Unicon/cas-addons"
# f = open('logs\\maven\\Unicon_cas-addons\\cas-addons-272-52354372.txt', 'r')

#errore test failed
# reponame="SomMeri/less4j"
# f = open('logs\\maven\\SomMeri_less4j\\less4j-919-109639390.txt', 'r')

#errore TODO vedi che ti becca anche una cosa zip snapshot
# reponame="Nodeclipse/nodeclipse-1"
# f = open('logs\\maven\\Nodeclipse_nodeclipse-1\\nodeclipse-1-304-75872733.txt', 'r')

#passed //sempre problema di quando ci sono i test....
# reponame="owlike/genson"
# f = open('logs\\maven\\owlike_genson\\genson-190-178485212.txt', 'r')

#passed
# reponame="reficio/p2-maven-plugin"
# f = open('logs\\maven\\reficio_p2-maven-plugin\\p2-maven-plugin-160-164806102.txt', 'r')

#errore
# reponame="teamed/qulice"
# f = open('logs\\maven\\teamed_qulice\\qulice-1329-180729613.txt', 'r')

#gradle
#passed
# reponame="jakenjarvis/Android-OrmLiteContentProvider"
# f = open('logs\\gradle\\jakenjarvis_Android-OrmLiteContentProvider\\Android-OrmLiteContentProvider-161-42820687.txt', 'r')

# #passed
# reponame="codecov/example-android"
# f = open('logs\\gradle\\square_picasso\\picasso-1351-174648005.txt', 'r')

#errore nelle dipendeze, no such file o directory
# reponame="rockerhieu/emojicon"
# f = open('logs\\gradle\\rockerhieu_emojicon\\emojicon-142-113999428.txt', 'r')

#lint error
# reponame="wasabeef/recyclerview-animators"
# f = open('logs\\gradle\\wasabeef_recyclerview-animators\\recyclerview-animators-180-80950913.txt', 'r')


#passed
# reponame="square/picasso"
# f = open('logs\\gradle\\square_picasso\\picasso-1352-174661345.txt', 'r')

#passed
# reponame="oblac/jodd"
# f = open('logs\\gradle\\oblac_jodd\\jodd-738-171756800.txt', 'r')

#passed ma fallito un comando non found task
# reponame="tilal6991/HoloIRC"
# f = open('logs\\gradle\\tilal6991_HoloIRC\\HoloIRC-261-85600415.txt', 'r')

#passed
# reponame="SimonVT/cathode"
# f = open('logs\\gradle\\SimonVT_cathode\\cathode-276-175366192.txt', 'r')

#passed
# reponame="oblac/jodd"
# f = open('logs\\gradle\\oblac_jodd\\jodd-739-174610217.txt', 'r')

#passed
# reponame="nohana/Laevatein"
# f = open('logs\\gradle\\nohana_Laevatein\\Laevatein-243-161336069.txt', 'r')

#lint error
# reponame="JFXtras/jfxtras-labs"
# f = open('logs\\gradle\\JFXtras_jfxtras-labs\\jfxtras-labs-237-44686312.txt', 'r')

# passed
# reponame="hamcrest/JavaHamcrest"
# f = open('logs\\gradle\\hamcrest_JavaHamcrest\\JavaHamcrest-293-149530896.txt', 'r')

#passed
# reponame="AzureAD/azure-activedirectory-library-for-android"
# f = open('logs\\gradle\\Azure\\azure-activedirectory-library-for-android-2686-180301575.txt', 'r')

#passed
# reponame="albertlatacz/java-repl"
# f = open('logs\\gradle\\albertlatacz_java-repl\\java-repl-429-164104426.txt', 'r')

#passed  +-
# reponame="Unidata/thredds"
# f = open('logs\\gradle\\Unidata_thredds\\thredds-4452-180125762.txt', 'r')

#passed
# reponame="kelemen/netbeans-gradle-project"
# f = open('logs\\gradle\\kelemen_netbeans-gradle-project\\netbeans-gradle-project-221-176155983.txt', 'r')

#stopped problema ci riprova tre volte e quindi mi leggo per tre volte i task
# reponame="RS485/LogisticsPipes"
# f = open('logs\\gradle\\RS485_LogisticsPipes\\LogisticsPipes-1552-171880899.txt', 'r')
#passed ****************************************************
# f = open('logs\\gradle\\RS485_LogisticsPipes\\LogisticsPipes-1553-174463961.txt', 'r')

#ruby
# reponame="opf/openproject"
# f = open('logs\\ruby\\openproject\\openproject-22428-176253633.txt', 'r')

#usa npm TODO capire come prendere i risultati
# reponame="zendesk/samson"
# f = open('logs\\ruby\\samson\\samson-7987-175874498.txt', 'r')

# #usa BRAKEMAN
# reponame="ManageIQ/manageiq"
# f = open('logs\\ruby\\ManageIQ\\manageiq-59083-175928155.txt', 'r')

#failures example
# reponame="rapid7/metasploit-framework"
# f = open('logs\\ruby\\metasploit-framework\\metasploit-framework-20590-175876290.txt', 'r')

# passed
# reponame="richpeck/exception_handler"
# f = open('logs\\ruby\\exception_handler\\exception_handler-1264-168008434.txt', 'r')

#linguaggio generic
# reponame="travis-ci/travis-cookbooks"
# f = open('logs\\ruby\\travis-cookbook\\travis-cookbooks-3486-175761182.txt', 'r')

#example failures
# reponame="codeforamerica/textizen"
# f = open('logs\\ruby\\codeforamerica_textizen\\textizen-198-68670428.txt', 'r')


#un log e' java e uno e' ruby.......
## exit 1 no rake file found
# reponame="ActiveJpa/activejpa"
# f = open('logs\\ruby\\ActiveJpa_activejpa\\activejpa-352-166258511.txt', 'r')
#maven
# f = open('logs\\ruby\\ActiveJpa_activejpa\\activejpa-353-166258664.txt', 'r')

reponame="atmos/heaven"
f = open('logs\\ruby\\atmos_heaven\\heaven-351-125806879.txt', 'r')

#passed solo pending examples
# reponame="bikeindex/bike_index"
# f = open('logs\\ruby\\bikeindex_bike_index\\bike_index-2319-179224411.txt', 'r')

#passed
# reponame="diaspora/diaspora"
# f = open('logs\\ruby\\diaspora_diaspora\\diaspora-11248-172674499.txt', 'r')

#Done job cancelled ......
# #gli altri log non finiscono proprio...restano appesi sui download
# reponame="elastic/logstash"
# f = open('logs\\ruby\\elastic_logstash\\logstash-5037-181542610.txt', 'r')

# reponame="jruby/warbler"
# f = open('logs\\ruby\\jruby_warbler\\warbler-428-135758385.txt', 'r')
# #log maven... con ruby
# f = open('logs\\ruby\\jruby_warbler\\warbler-429-141828088.txt', 'r')


#errori negli example
# reponame="loomio/loomio"
# f = open('logs\\ruby\\loomio_loomio\\loomio-12955-181473783.txt', 'r')


#passed
# reponame="MagLev/maglev"
# f = open('logs\\ruby\\MagLev_maglev\\maglev-754-103350661.txt', 'r')

#passed
# reponame="progit/progit"
# f = open('logs\\ruby\\progit_progit\\progit-1328-126799418.txt', 'r')

# reponame="puppetlabs/puppet"
# f = open('logs\\ruby\\puppetlabs_puppet\\puppet-12769-181370799.txt', 'r')
# # rake aborted!
# f = open('logs\\ruby\\puppetlabs_puppet\\puppet-12769-181370800.txt', 'r')

# #errored example fallito
# reponame="refinery/refinerycms"
# f = open('logs\\ruby\\refinery_refinerycms\\refinerycms-3396-181230356.txt', 'r')

#passed solo example pending
# reponame="psu-stewardship/scholarsphere"
# f = open('logs\\ruby\\psu-stewardship_scholarsphere\\scholarsphere-4008-175444363.txt', 'r')

#rubocop failed!
# reponame="shoes/shoes4"
# f = open('logs\\ruby\\shoes_shoes4\\shoes4-3259-180295136.txt', 'r')

# reponame="saberma/shopqi"
# f = open('logs\\ruby\\saberma_shopqi\\shopqi-936-3054294.txt', 'r')

#errore di dipendenze gem file missing
# reponame="sunlightlabs/scout"
# f = open('logs\\ruby\\sunlightlabs_scout\\scout-1110-92726320.txt', 'r')

#test failure
# reponame="saberma/shopqi"
# f = open('logs\\ruby\\saberma_shopqi\\shopqi-935-3044868.txt', 'r')
#
#test failre e dependencies error
# reponame="pophealth/popHealth"
# f = open('logs\\ruby\\pophealth_popHealth\\popHealth-633-55248730.txt', 'r')
#
#passed
# reponame="expertiza/expertiza"
# f = open('logs\\ruby\\expertiza_expertiza\\expertiza-4273-180323840.txt', 'r')
#
#passed
# reponame="github/gemoji"
# f = open('logs\\ruby\\github_gemoji\\gemoji-173-171951584.txt', 'r')
#
# rubocop failures
# reponame="prawnpdf/prawn"
# f = open('logs\\ruby\\prawnpdf_prawn\\prawn-1317-175634877.txt', 'r')

# Gem error
# reponame="makrio/makrio"
# f = open('logs\\ruby\\makrio_makrio\\makrio-880-362508.txt', 'r')

#passed
# reponame="jeremyevans/sequel"
# f = open('logs\\ruby\\jeremyevans_sequel\\sequel-795-181626601.txt', 'r')

# reponame="aws/aws-sdk-ruby"
# f = open('logs\\ruby\\aws_aws-sdk-ruby\\aws-sdk-ruby-3267-182023831.txt', 'r')
#
# passed
# reponame="openfoodfoundation/openfoodnetwork"
# f = open('logs\\ruby\\openfoodfoundation_openfoodnetwork\\openfoodnetwork-3698-182106675.txt', 'r')
#
#test failure
# reponame="sparklemotion/nokogiri"
# f = open('logs\\ruby\\sparklemotion_nokogiri\\nokogiri-1183-179374208.txt', 'r')
#
#errored
# reponame="aprescott/serif"
# f = open('logs\\ruby\\aprescott_serif\\serif-381-66444505.txt', 'r')
# reponame="aprescott/serif"
# f = open('logs\\ruby\\aprescott_serif\\serif-382-142280315.txt', 'r')

#passed
# reponame="railsbridge/docs"
# f = open('logs\\ruby\\railsbridge_docs\\docs-1095-175616897.txt', 'r')

#passed
# reponame="ari/jobsworth"
# f = open('logs\\ruby\\ari_jobsworth\\jobsworth-1072-119894436.txt', 'r')

# reponame="fog/fog"
# f = open('logs\\ruby\\fog_fog\\fog-5825-169882320.txt', 'r')

#rake aborted
# reponame="projectblacklight/blacklight"
# f = open('logs\\ruby\\projectblacklight_blacklight\\blacklight-4582-181660471.txt', 'r')

# reponame="cloudfoundry/cloud_controller_ng"
# f = open('logs\\ruby\\cloudfoundry_cloud_controller_ng\\cloud_controller_ng-7177-181964132.txt', 'r')

# reponame="MarkUsProject/Markus"
# f = open('logs\\ruby\\MarkUsProject_Markus\\Markus-3485-182033902.txt', 'r')

#errored install
# reponame="twitter/twitter-cldr-rb"
# f = open('logs\\ruby\\twitter_twitter-cldr-rb\\twitter-cldr-rb-1166-181089150.txt', 'r')

#failed
# reponame="middleman/middleman"
# f = open('logs\\ruby\\middleman_middleman\\middleman-2625-179389930.txt', 'r')

#rubocop failed
# reponame="sferik/twitter"
# f = open('logs\\ruby\\sferik_twitter\\twitter-1672-181214912.txt', 'r')


# reponame="errbit/errbit"
# #exit with 1
# # f = open('logs\\ruby\\errbit_errbit\\errbit-1877-177799297.txt', 'r')
# #errored
# f = open('logs\\ruby\\errbit_errbit\\errbit-1878-181893816.txt', 'r')

#passed
# reponame="neo4jrb/neo4j-core"
# f = open('logs\\ruby\\neo4jrb_neo4j-core\\neo4j-core-1872-182009469.txt', 'r')

# reponame="locomotivecms/engine"
# f = open('logs\\ruby\\locomotivecms_engine\\engine-1332-181220897.txt', 'r')

# reponame="ging/social_stream"
# f = open('logs\\ruby\\ging_social_stream\\social_stream-2334-150958722.txt', 'r')

#test failed
# reponame="fatfreecrm/fat_free_crm"
# f = open('logs\\ruby\\fatfreecrm_fat_free_crm\\fat_free_crm-1874-176518429.txt', 'r')

#passed no tool matched
# reponame="browsermedia/browsercms"
# f = open('logs\\ruby\\browsermedia_browsercms\\browsercms-244-169634664.txt', 'r')

# reponame="innoq/iqvoc"
#gem error
# f = open('logs\\ruby\\innoq_iqvoc\\iqvoc-1215-183937349.txt', 'r')

# reponame="rubygems/rubygems"
# f = open('logs\\ruby\\rubygems_rubygems\\rubygems-3920-181365330.txt', 'r')

# reponame="hacketyhack/hackety-hack.com"
# f = open('logs\\ruby\\hacketyhack_hackety-hack.com\\hackety-hack.com-257-92540002.txt', 'r')

#passed
# reponame="grosser/parallel_tests"
# f = open('logs\\ruby\\grosser_parallel_tests\\parallel_tests-653-181173737.txt', 'r')
#
#passed
# reponame="codeforamerica/citygram"
# f = open('logs\\ruby\\codeforamerica_citygram\\citygram-818-153766098.txt', 'r')

# reponame="sferik/rails_admin"
# f = open('logs\\ruby\\sferik_rails_admin\\rails_admin-2376-181954062.txt', 'r')

# reponame="twers/re-education"
# f = open('logs\\ruby\\twers_re-education\\re-education-162-2271090.txt', 'r')
#
# reponame="newrelic/rpm"
# f = open('logs\\ruby\\newrelic_rpm\\rpm-609-181875494.txt', 'r')
#
# reponame="calagator/calagator"
# f = open('logs\\ruby\\calagator_calagator\\calagator-1037-158304927.txt', 'r')

# reponame="asciidoctor/asciidoctor-diagram"
# f = open('logs\\ruby\\asciidoctor_asciidoctor-diagram\\asciidoctor-diagram-267-183778861.txt', 'r')

# reponame="mitchellh/vagrant"
# f = open('logs\\ruby\\mitchellh_vagrant\\vagrant-6965-184196955.txt', 'r')





def getBuildId(f):
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    index= s.find('Build id:')
    if index !=-1:
        s.seek(index)
        id=s.readline().split(":")[1].strip()
        return id
    else:
        print "Error: non e' possibile prendere la build id dal log......"
        return -1



b=common_parse(reponame, getBuildId(f))
print "\nLOG"
linguaggio= b.getLanguage()
#TODO c'e' il caso di language: generic   -.-'
if linguaggio== "ruby":
    #supponiamo che si usa solo rake e che non usano maven
    rubyLog=parserRuby(f,RubyLog(reponame))
    print rubyLog.toJSON()
else:
    tool=checkGradleMavenFile(f)
    if(tool=="maven"):
        mavenLog=parserMaven(f, MavenLog(reponame))
        print mavenLog.toJSON()
    elif(tool=="gradle"):
        gradleLog=parserGradle(f, GradleLog(reponame))
        print gradleLog.toJSON()
print ("PARSE END")