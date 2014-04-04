from xml.sax import ContentHandler

__author__ = 'brent'


class KennyGSAXHandler(ContentHandler):
    def __init__(self, action_tree, verbose=False, *args, **kwargs):
        # ContentHandler is an old-school class and does not inherit from object
        # super(KennyGSAXHandler, self).__init__(*args, **kwargs)
        self.action_tree = action_tree
        self.current_tree = []
        self.verbose = verbose
        self.ALLTAGS = '*'

    def is_valid(self, name=None):
        """
        Check to see if the current xml path is to be processed.
        """
        valid_tags = self.action_tree
        invalid = False
        for item in self.current_tree:
            try:
                valid_tags = valid_tags[item if item in valid_tags else self.ALLTAGS] \
                    if item in valid_tags or self.ALLTAGS in valid_tags else None
                # DEBUG print self.current_tree, item, valid_tags
            except (KeyError, TypeError) as _:  # object is either missing the key or is not a dictionary type
                invalid = True
                break
        return not invalid and valid_tags is not None

    def get_action_obj(self, action):
        action_tree = self.action_tree
        found = True
        for item in self.current_tree:
            try:
                if item in action_tree or self.ALLTAGS in action_tree:
                    try:
                        action_tree = action_tree[item if item in action_tree else self.ALLTAGS]
                    except KeyError as _:  # action_tree is missing this item and does not contain ALLTAGS
                        found = False
                        break
                else:
                    found = False
                    break
            except TypeError as _: # action_tree is not of type dictionary
                found = False
                break
        return action_tree if found else None

    def action(self, action, *values, **kwargs):
        action_obj = self.get_action_obj(action)
        if action_obj is not None and hasattr(action_obj, action):
            # Will throw a type error if an element has a value or attributes and the provided
            #  function does not except values or those keyword arguments
            getattr(action_obj, action)(*values, **kwargs)
        elif action_obj is not None and type(action_obj) == dict and action in action_obj:
            # Will throw an exception if action is not a function, or does not take the arguments provided
            action_obj[action](*values, **kwargs)


    def startElement(self, name, attrs):
        self.current_tree.append(name)
        if self.is_valid():
            self.current_value = ""
            if self.verbose:
                print("    " * len(self.current_tree) + name )
            self.action('start')


    def endElement(self, name):
        if self.is_valid():
            if self.verbose:
                print("    " * len(self.current_tree) + name )
            self.action('value', self.current_value)
            self.action('end')
        p = self.current_tree.pop()
        assert p == name


    def characters(self, content):
        if self.is_valid():
            if self.verbose and len(content.strip()):
                print("    " * (len(self.current_tree) + 1) + content)
            self.current_value += content


