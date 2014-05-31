@GrabResolver('https://artifactory.tagged.com/artifactory/libs-release-local/')
@Grab('com.tagged.build:jenkins-dsl-common:0.1.18')

import com.tagged.build.common.*

def twemproxy_project = new Project(
    jobFactory,
    [
        githubOwner: 'jdi-tagged',
        githubProject: 'twemproxy',
        githubHost: 'github.com',
        hipchatRoom:'Pets',
        email: 'jirwin@tagged.com'
    ]
)

def twemproxy = twemproxy_project.downstreamJob(defaultRef: 'build') {
    description "Builds our fork of twemproxy from https://github.com/jdi-tagged/twemproxy"
    jdk 'default'
    label 'orc01'
    steps{
        shell '''bash << _EOF_
autoreconf -fvi
./configure
make dist
rm -rf SOURCES SPECS BUILD BUILDROOT RPMS SRPMS
mkdir SOURCES
mv nutcracker*tar.gz SOURCES
echo workspace "$WORKSPACE"
rpmbuild \\
           --define "_topdir $WORKSPACE" \\
           --define "release `date +%Y%m%d%H%M%S`" \\
           -ba scripts/nutcracker.spec
_EOF_'''
    }
    triggers {
        githubPush()
        scm('5 * * * *')
    }
    publishers {          // mailer(String recipients, String dontNotifyEveryUnstableBuildBoolean = false, String sendToIndividualsBoolean = false)
        mailer(twemproxy_project.notifyEmail, true, true)
        archiveArtifacts('**/*.rpm')
    }
    hipchat(twemproxy_project.hipchatRoom, false)
}
