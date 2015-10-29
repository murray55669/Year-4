#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET


test = ["""<row Id="4" PostTypeId="1" AcceptedAnswerId="7" CreationDate="2008-07-31T21:42:52.667" Score="264" ViewCount="16201" Body="&lt;p&gt;I want to use a track-bar to change a form's opacity.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;This is my code:&lt;/p&gt;&#xA;&#xA;&lt;pre&gt;&lt;code&gt;decimal trans = trackBar1.Value / 5000;&#xA;this.Opacity = trans;&#xA;&lt;/code&gt;&lt;/pre&gt;&#xA;&#xA;&lt;p&gt;When I try to build it, I get this error:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;Cannot implicitly convert type 'decimal' to 'double'.&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;I tried making &lt;strong&gt;trans&lt;/strong&gt; to &lt;strong&gt;double&lt;/strong&gt;, but then the control doesn't work. This code has worked fine for me in VB.NET in the past. &lt;/p&gt;&#xA;" OwnerUserId="8" LastEditorUserId="2648239" LastEditorDisplayName="Rich B" LastEditDate="2014-01-03T02:42:54.963" LastActivityDate="2014-01-03T02:42:54.963" Title="When setting a form's opacity should I use a decimal or double?" Tags="&lt;c#&gt;&lt;winforms&gt;&lt;forms&gt;&lt;type-conversion&gt;&lt;opacity&gt;" AnswerCount="13" CommentCount="2" FavoriteCount="25" CommunityOwnedDate="2012-10-31T16:42:47.213" />"""]

#for line in test:
for line in sys.stdin:
    line = line.strip()
    root = ET.fromstring(line)
    if int(root.attrib['PostTypeId']) == 1:
        print "{0}\t{1}".format(root.attrib['ViewCount'], root.attrib['Id'])