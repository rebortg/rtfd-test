import sys
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


def setup(app):
    app.add_node(CmdNode, html=(CmdNode.visit_div, CmdNode.depart_div))
    app.add_directive('cfgcmd', CfgCmdDirective)
    app.add_directive('opcmd', OpCmdDirective)


class CmdNode(nodes.General, nodes.Element): 

  
    @staticmethod
    def visit_div(self, node):
        self.body.append(self.starttag(node, 'div'))
    
    @staticmethod
    def depart_div(self, node=None):
        self.body.append('</div>\n')
   

class CmdDirective(Directive):

    """
        generic Panel directive class definition.
        This class define a directive that shows 
        bootstrap Labels around its content
        *usage:*
            .. panel-<panel-type>:: 
                :title: <title>
                <Panel content>
        *example:*
            .. panel-default:: 
                :title: panel title
                This is a default panel content
    """

    has_content = True
    option_spec = {
        'cmd': directives.unchanged,
    }
    custom_class = ''

    def run(self):
        idb = nodes.make_id(self.custom_class+"cmd-" + self.options["cmd"])
        target = nodes.target(ids=[idb])

        # First argument is the name of the glyph
        panel_name = 'cmd-{}'.format(self.custom_class)
        # get the label title
        title_text = self.options.get('cmd', self.custom_class.title())
        # get the label content
        text = '\n'.join(self.content)
        # Create the panel element
        panel_element = CmdNode()
        panel_element['classes'] += ['cmd', panel_name]
        # Create the panel headings
        heading_element = CmdNode(title_text)
        title_nodes, messages = self.state.inline_text(title_text,
                                                       self.lineno)
        title = nodes.paragraph(title_text, '', *title_nodes)
        heading_element.append(target)
        heading_element.append(title)
        heading_element['classes'] += [self.custom_class+'cmd-heading']
        # Create a new container element (div)
        body_element = CmdNode(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                body_element)
        # Set its custom bootstrap classes
        body_element['classes'] += [self.custom_class+'cmd-body']
        # add the heading and body to the panel
        panel_element.append(heading_element)
        panel_element.append(body_element)
        # Return the panel element
        return [panel_element]

class OpCmdDirective(CmdDirective):

    custom_class = 'op'

class CfgCmdDirective(CmdDirective):

    custom_class = 'cfg'
