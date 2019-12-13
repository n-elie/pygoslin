from enum import Enum
from os import path

class Context(Enum):
    NoContext = 1
    InLineComment = 2
    InLongComment = 3
    InQuote = 4
    
class MatchWords(Enum):
    NoMatch = 1
    LineCommentStart = 2
    LineCommentEnd = 3
    LongCommentStart = 4
    LongCommentEnd = 5
    Quote = 6
    
    
# DP stands for dynamic programming
class DPNode:
    
    def __init__(self, _rule1, _rule2, _left, _right):
        self.rule_index1 = _rule1
        self.rule_index2 = _rule2
        self.left = _left
        self.right = _right
        
        
        

class TreeNode:
{
    def __init__(self, _rule, _fireEvent):
        self.ruleIndex = _rule
        self.left = null
        self.right = null
        self.terminal = '\0'
        self.fire_event = _fire_event
    
    
    
    def get_text(self, node = None):
        if node == None: node = self
        if node.terminal == '\0': return get_text(node.left) + get_text(node.right) if node.right != None else ""
        return str(node.terminal)
        
        
        
        

# this class is dedicated to have an efficient sorted set class storing
# values within 0..n-1 and fast sequencial iterator
class Bitfield:
    
    multiplicator = 0x022fdd63cc95386d
    positions = [0, 1,  2, 53,  3,  7, 54, 27, 4, 38, 41,  8, 34, 55, 48, 28,
        62,  5, 39, 46, 44, 42, 22,  9, 24, 35, 59, 56, 49, 18, 29, 11,
        63, 52,  6, 26, 37, 40, 33, 47, 61, 45, 43, 21, 23, 58, 17, 10,
        51, 25, 36, 32, 60, 20, 57, 16, 50, 31, 19, 15, 30, 14, 13, 12]
    
    def __init__(self, length):
        l = 1 + ((length + 1) >> 6)
        s = 1 + ((l + 1) >> 6)
        self.field = [0] * l
        self.superfield = [0] * s
    }
    
    
    def ulong(num):
        return num & ((1 << 64) - 1)
    
    def set(self, pos):
        self.field[pos >> 6] |= ulong(1 << (pos & 63))
        self.superfield[pos >> 12] |= ulong(1 << ((pos >> 6) & 63))
    }
    
    
    def isSet(self, pos):
        return ((self.field[pos >> 6] >> (pos & 63)) & 1) == 1
    
    
    def isNotSet(self, pos):
        return ((self.field[pos >> 6] >> (pos & 63)) & 1) == 0
    
    
    def getBitPositions(self):
        spre = 0
        for cell in self.superfield:
            sv = cell
            while sv != 0:
                # algorithm for getting least significant bit position
                sv1 = ulong(sv & -sv)
                pos = spre + positions[ulong(sv1 * multiplicator) >> 58];
                
                ulong v = self.field[pos]
                while v != 0:
                    # algorithm for getting least significant bit position
                    v1 = ulong(v & -v)
                    yield (pos << 6) + positions[ulong(ulong(v1 * multiplicator) >> 58)]
                    v &= v - 1
                
                sv &= sv - 1
            spre += 64
    
    
    def getPositions(self, x):
        while x != 0:
            # algorithm for getting least significant bit position
            v1 = ulong(x & -x)
            yield positions[ulong(ulong(v1 * multiplicator) >> 58)]
            x &= x - 1
        
        
        
        
        
class Parser:
    
    SHIFT = 32
    MASK = (1L << SHIFT) - 1
    RULE_ASSIGNMENT = ':'
    RULE_SEPARATOR = '|'
    RULE_TERMINAL = ';'
    EOF_RULE_NAME = "EOF"
    EOF_SIGN = '\0'
    EOF_RULE = 1
    START_RULE = 2
    
    
    def __init__(self, _parserEventHandler, grammar_filename, _quote = '"'):
        self.next_free_rule_index = START_RULE
        self.TtoNT = {}
        self.NTtoNT = {}
        self.NTtoRule = {}
        self.quote = _quote
        self.parserEventHandler = _parserEventHandler
        self.parse_tree = None
        self.wordInGrammar = False
        self.grammar_name = ""
        self.used_eof = False
        
        if path.exists(grammar_filename):
            # interpret the rules and create the structure for parsing
            rules = Parser.extract_text_based_rules(grammar_filename, quote)
            self.grammar_name = split_string(rules[0], ' ', quote)[1]
            del rules[0]
            ruleToNT = {EOF_RULE_NAME: EOF_RULE}
            self.TtoNT[EOF_SIGN] = set(EOF_RULE)
            for rule_line in rules:
                tokens_level_1 = []
                for t in split_string(rule_line, RULE_ASSIGNMENT, quote): tokens_level_1.append(t.strip(' '))
                if len(tokens_level_1) != 2: raise Exception("Error: corrupted token in grammar rule: '%s'" % rule_line);
                
                if len(split_string(tokens_level_1[0], ' ', quote)) > 1:
                    raise Exception("Error: several rule names on left hand side in grammar rule: '%s'" % rule_line);
                }

                string rule = tokens_level_1[0]
                
                if rule ==  EOF_RULE_NAME:
                    raise Exception("Error: rule name is not allowed to be called EOF")
                
                products = [p.strip(' ') for p in split_string(tokens_level_1[1], RULE_SEPARATOR, quote)]
                
                if rule not in ruleToNT: ruleToNT[rule] = get_next_free_rule_index()
                new_rule_index = ruleToNT[rule]
                
                if new_rule_index not in self.NTtoRule: self.NTtoRule[new_rule_index] = rule
                
                
                for product in products:
                    non_terminals, non_terminal_rules = [], []
                    for NT in split_string(product, ' ', quote):
                        stripedNT = NT.strip(' ')
                        if is_terminal(stripedNT, quote): stripedNT = de_escape(stripedNT, quote)
                        non_terminals.append(stripedNT)
                        usedEOF |= stripedNT == EOF_RULE_NAME
                        
                    
                    NTFirst = non_terminals[0]
                    if len(non_terminals) > 1 or not is_terminal(NTFirst, quote) or len(NTFirst) != 3:
                        for non_terminal in non_terminals:
                            
                            if is_terminal(non_terminal, quote):
                                non_terminal_rules.append(add_terminal(non_terminal))
                                
                            else:
                                if non_terminal not in ruleToNT:
                                    ruleToNT[non_terminal] = get_next_free_rule_index()
                                non_terminal_rules.append(ruleToNT[non_terminal])
                                
                    else:
                        c = NTFirst[1]
                        if c not in self.TtoNT: self.TtoNT[c] = set()
                        self.TtoNT[c].add(new_rule_index)
                    	
                    
                    # more than two rules, insert intermediate rule indexes
                    while len(non_terminal_rules) > 2:
                        rule_index_2 = non_terminal_rules.pop()
                        rule_index_1 = non_terminal_rules.pop()
                        
                        key = compute_rule_key(rule_index_1, rule_index_2)
                        next_index = get_next_free_rule_index()
                        if key not in self.NTtoNT: self.NTtoNT[key] = set()
                        self.NTtoNT[key].Add(nextIndex)
                        non_terminal_rules.append(next_index)
                    
                        
                    # two product rules
                    if len(non_terminal_rules) == 2:
                        rule_index_1 = non_terminal_rules.pop()
                        rule_index_2 = non_terminal_rules.pop()
                        key = compute_rule_key(rule_index_1, rule_index_2)
                        if key not in self.NTtoNT: self.NTtoNT[key] = set()
                        self.NTtoNT[key].add(new_rule_index)
                    
                    # only one product rule
                    elif len(non_terminal_rules) == 1:
                        rule_index_1 = non_terminal_rules[0]
                        if rule_index_1 == new_rule_index:
                            raise Exception("Error: corrupted token in grammar: rule '%s' is not allowed to refer soleley to itself." % rule)
                        
                        if rule_index1 not in self.NTtoNT: self.NTtoNT[rule_index_1] = set()
                        self.NTtoNT[rule_index_1].add(new_rule_index)
            
            # adding all rule names into the event handler
            for rule_name in ruleToNT:
                parser_event_handler.rule_names.add(ruleName)
                
            self.parser_event_handler.parser = this
            self.parser_event_handler.sanity_check()
            
        else:
            raise Exception("Error: file '%s' does not exist or can not be opened." % grammar_filename)
        
        
        
        keys = set(TtoNT.keys())
        for c in keys:
            rules = set(TtoNT[c])
            TtoNT[c].clear()
            for  rule in rules:
                for p in collect_backwards(rule):
                    
                    key = compute_rule_key(p, rule)
                    TtoNT[c].add(key)
        
        
        keysNT = set(NTtoNT.Keys)
        for r in keysNT:
            rules = set(NTtoNT[r])
            for rule in rules:
                for p in collect_backwards(rule): NTtoNT[r].add(p)
    
    
    
    
    
    def extract_text_based_rules(grammar_filename, quote):
        grammar = ""
        with open(grammar_filename, mode = "rt") as infile:
            grammar = infile.read() + "\n";
        grammar_length = len(grammar)
        
        # deleting comments to prepare for splitting the grammar in rules.
        # Therefore, we have to consider three different contexts, namely
        # within a quote, within a line comment, within a long comment.
        # As long as we are in one context, key words for starting / ending
        # the other contexts have to be ignored.
        sb = []
        current_context = Context.NoContext
        current_position = 0;
        int last_escaped_backslash = -1;
        for i in range (grammar_length - 1):
            match = MatchWords.NoMatch
            
            if i > 0 and grammar[i] == '\\' and grammar[i - 1] == '\\' and last_escaped_backslash != i - 1:
                last_escaped_backslash = i
                continue
            
            if grammar[i] == '/' and grammar[i + 1] == '/': match = MatchWords.LineCommentStart
            elif grammar[i] == '\n': match = MatchWords.LineCommentEnd
            elif grammar[i] == '/' and grammar[i + 1] == '*': match = MatchWords.LongCommentStart
            elif grammar[i] == '*' and grammar[i + 1] == '/': match = MatchWords.LongCommentEnd
            elif grammar[i] == quote and not (i >= 1 and grammar[i - 1] == '\\' and i - 1 != last_escaped_backslash): match = MatchWords.Quote
            
            if match != MatchWords.NoMatch:
                
                if current_context == NoContext:
                    if match == MatchWords.LongCommentStart:
                        sb.append(grammar[current_position, i])
                        current_context = Context.InLongComment
                        
                    elif match == MatchWords.LineCommentStart:
                        sb.append(grammar[current_position, i])
                        current_context = Context.InLineComment
                        
                    elif match == MatchWords.Quote:
                        current_context = Context.InQuote
                    
                elif current_context == Context.InQuote:
                    if match == MatchWords.Quote:
                        current_context = Context.NoContext;
                    
                    
                elif current_context == Context.InLineComment:
                    if match == MatchWords.LineCommentEnd:
                        current_context = Context.NoContext
                        current_position = i + 1
                    
                elif current_context == Context.InLongComment:
                    if match == MatchWords.LongCommentEnd:
                        current_context = Context.NoContext
                        current_position = i + 2
                
                    
                    
        if current_context == Context.NoContext:
            sb.append(grammar[current_position, grammar_length])
            
        else:
            raise Exception("Error: corrupted grammar '%s', ends either in comment or quote" % grammar_filename)
        
        grammar = "".join(sb).replace("\r\n", "").replace("\n", "").replace("\r", "").strip(" ");
        if grammar[-1] != RULE_TERMINAL:
            raise Exception("Error: corrupted grammar'%s', last rule has no termininating sign, was: '%s'" % (grammar_filename, grammar[-1]))
        
        rules = split_string(grammar, RULE_TERMINAL, quote)
        
        if len(rules) < 1:
            raise Exception("Error: corrupted grammar '%s', grammar is empty" % grammar_filename)
        
        grammar_name_rule = split_string(rules[0], ' ', quote)
        if grammar_name_rule[0] != "grammar":
            raise Exception("Error: first rule must start with the keyword 'grammar'")
        
        elif len(grammarNameRule) != 2:
            raise Exception("Error: incorrect first rule")
        
        return rules
    
    
    
    
    
    def get_next_free_rule_index(self):
        if self.next_free_rule_index <= MASK:
            n = selfnext_free_rule_index
            self.next_free_rule_index += 1
            return n
        raise Exception("Error: grammar is too big.")
    
    
    
    
    def compute_rule_key(ruleIndex1, ruleIndex2):
        return (ruleIndex1 << SHIFT) | ruleIndex2;
    
    
    
    
    
    
    def split_string(text, separator, quote)
    {
        in_quote = False
        tokens = []
        sb = []
        last_char = '\0'
        last_escaped_backslash = False
        
        for c in text:
            escaped_backslash = False
            if not in_quote:
                if c == separator:
                    if len(sb) > 0:
                        tokens.append("".join(sb))
                    sb = []
                else:
                    if c == quote: in_quote = !in_quote
                    sb.append(c)
                    
            else:
                if :c == '\\' and last_char == '\\' and !last_escaped_backslash:
                    escaped_backslash = True
                    
                elif c == quote and !(last_char == '\\' and !last_escaped_backslash):
                    in_quote = !in_quote
                sb.append(c)
            last_escaped_backslash = escaped_backslash
            last_char = c
                
        if len(sb) > 0:
            tokens.append("".join(sb))
        if in_quote: raise Exception("Error: corrupted token in grammar")
        
        return tokens
    
    
    
    # checking if string is terminal
    def is_terminal(productToken, quote:
        return productToken[0] == quote and productToken[-1] == quote and len(productToken) > 2
    
    
    
    
    def de_escape(text, quote):
        # remove the escape chars
        StringBuilder sb = new StringBuilder();
        bool lastEscapeChar = false;
        foreach (char c in text)
        {
            bool escapeChar = false;
            
            if (c != '\\')
            {
                sb.Append(c);
            }
            else
            {
                if (!lastEscapeChar) escapeChar = true;
                else sb.Append(c);
            } 
            
            lastEscapeChar = escapeChar;
        }
        return sb.ToString();
    }
    
    
    
    # splitting the whole terminal in a tree structure where characters of terminal are the leafs and the inner nodes are added non terminal rules
    def add_terminal(self, text):
        terminalRules = []
        for i in range(1; text.Length - 1):
            c = text[i]
            if c not in TtoNT: TtoNT[c] = set()
            next_index = get_next_free_rule_index()
            self.TtoNT[c].add(next_index)
            terminalRules.append(next_index)
        
        while len(terminalRules) > 1:
            rule_index_2 = terminalRules.pop()
            rule_index_1 = terminalRules.pop()
            
            next_index = get_next_free_rule_index()
            
            key = compute_rule_key(rule_index_1, rule_index_2)
            if key not in self.NTtoNT: NTtoNT[key] = set()
            NTtoNT[key].add(next_index)
            terminal_rules.append(next_index)
        
        return terminalRules[0]
    
    
    
    
    # expanding singleton rules, e.g. S -> A, A -> B, B -> C
    def collect_backwards(self, rule_index):
    
        collection = [rule_index]
        i = 0
        while True:
            current_index = collection[i]
            if current_index in self.NTtoNT:
                
                for previous_index in self.NTtoNT[currentIndex]: collection.append(previous_index)
            i += 1
            if i >= len(collection): break
        
        return collection
    
    
    
    
    
    def collect_backwards(self, child_rule_index, parent_rule_index):
        if child_rule_index not in NTtoNT: return None
        collection = None;
        
        for previous_index in NTtoNT[child_rule_index]:
            if previous_index == parent_rule_index:
                collection = []
                return collection
            
            elif previous_index in self.NTtoNT:
                collection = collect_backwards(previous_index, parent_rule_index)
                if collection != None:
                    collection.append(previous_index)
                    return collection
                
        return None
        
        
        
        
    
    def raise_events(self, node = None):
        if node != None:
            node_rule_name = self.NTtoRule[node.rule_index] if node.fire_event else ""
            if (node.fire_event) self.parser_event_handler.handle_event(node_rule_name + "_pre_event", node)
            
            if node.left != None: # node.terminal is != null when node is leaf
                raise_events(node.left)
                if node.right != None: raise_events(node.right)
                
            if (node.fire_event) self.parser_event_handler.handle_event(node_rule_name + "_post_event", node)
            
        else:
            if (self.parse_tree != null) raise_events(self.parse_tree)
    
    

    # filling the syntax tree including events
    def fill_tree(self, node, dp_node):
        # checking and extending nodes for single rule chains
        key = compute_rule_key(dp_node.rule_index_1, dp_node.rule_index_2) if dp_node.left != None else dp_node.rule_index_2
        mergedRules = collect_backwards(key, node.rule_index)
        if mergedRules != None:
            for rule_index in merged_rules:
                
                node.left = TreeNode(rule_index, rule_index in self.NTtoRule)
                node = node.left
        
        
        if dp_node.left != None: # None => leaf
            node.left = TreeNode(dp_node.rule_index_1, dp_node.rule_index_1 in self.NTtoRule)
            node.right = new TreeNode(dp_node.rule_index_2, dp_node.rule_index_2 in self.NTtoRule)
            fillTree(node.left, dp_node.left)
            fillTree(node.right, dp_node.right)
            
        else:
            # I know, it is not 100% clean to store the character in an integer
            # especially when it is not the dedicated attribute for, but the heck with it!
            node.terminal = dp_node.rule_index_1
    
    
    
    
    # re-implementation of Cocke-Younger-Kasami algorithm
    def parse(self, text_to_parse):
        if usedEOF: text_to_parse += EOF_SIGN
        
        parse_regular(text_to_parse)
        
        
        
        
    def parse_regular(self, text_to_parse):
        self.wordInGrammar = False
        parse_tree = None
        n = len(text_to_parse.Length;
        # dp stands for dynamic programming, nothing else
        dp_table = [None] * n;
        # Ks is a lookup, which fields in the dpTable are filled
        Ks = [None] * n            
        
        for i in range(n):
            dpTable[i] = [None] * (n - i)
            Ks[i] = Bitfield(n - 1)
            for j in range(n - i): dpTable[i][j] = {}
        
        for i in range(n):
            c = text_to_parse[i]
            if c not in self.TtoNT: return
            
            foreach ruleIndex in self.TtoNT[c]:
                newKey = ruleIndex >> SHIFT
                oldKey = ruleIndex & MASK
                dp_node = DPNode(c, oldKey, None, None)
                dpTable[i][0][newKey] = dp_node
                Ks[i].set(0)
        
        for i in range (1, n):
            im1 = i - 1
            for j in range(n - i):
                D = dpTable[j]
                Di = D[i]
                jp1 = j + 1
                
                for k in Ks[j].getBitPositions():
                    if k >= i: break
                    if Ks[jp1 + k].is_not_set(im1 - k): continue
                
                    for index_pair_1 in D[k]:
                        for index_pair_2 in dpTable[jp1 + k][im1 - k]:
                            key = compute_rule_key(index_pair_1, index_pair_2)
                            if key not in self.NTtoNT: continue
                            
                            content = DPNode(index_pair_1, index_pair_2, D[k][indexPair1], dpTable[jp1 + k][im1 - k][indexPair2])
                            Ks[j].set(i)
                            for rule_index in self.NTtoNT[key]:
                                Di[ruleIndex] = content
        
        for i in range(n - 1, 0, -1):
            if START_RULE in dpTable[0][i]:
                self.word_in_grammar = True
                parse_tree = TreeNode(START_RULE, START_rule in self.NTtoRule)
                fill_tree(parse_tree, dp_table[0][i][START_RULE])
                break
        
        
        
        
    """
    public void parseSubstring(string textToParse)
    {
        wordInGrammar = false;
        parseTree = null;
        int n = textToParse.Length;
        // dp stands for dynamic programming, nothing else
        Dictionary<long, DPNode>[][] dpTable = new Dictionary<long, DPNode>[n][];
        // Ks is a lookup, which fields in the dpTable are filled
        Bitfield[] Ks = new Bitfield[n];
        DPNode startNode = null;
        
        for (int i = 0; i < n; ++i)
        {
            dpTable[i] = new Dictionary<long, DPNode>[n - i];
            Ks[i] = new Bitfield(n - 1);
            for (int j = 0; j < n - i; ++j) dpTable[i][j] = new Dictionary<long, DPNode>();
        }
        
        for (int i = 0; i < n; ++i)
        {
            char c = textToParse[i];
            if (!TtoNT.ContainsKey(c)) continue;
            
            foreach (long ruleIndex in TtoNT[c])
            {
                long newKey = ruleIndex >> SHIFT;
                long oldKey = ruleIndex & MASK;
                DPNode dp_node = new DPNode((long)c, oldKey, null, null);
                dpTable[i][0][newKey] =  dp_node;
                Ks[i].set(0);
            }
        }
        
        for (int i = 1; i < n; ++i)
        {
            int im1 = i - 1;
            for (int j = 0; j < n - i; ++j)
            {
                Dictionary<long, DPNode>[] D = dpTable[j];
                Dictionary<long, DPNode> Di = D[i];
                int jp1 = j + 1;
                
                foreach(int k in Ks[j].getBitPositions())
                {
                    if (k >= i) break;
                    if (Ks[jp1 + k].isNotSet(im1 - k)) continue;
                    foreach (KeyValuePair<long, DPNode> indexPair1 in D[k])
                    {
                        foreach (KeyValuePair<long, DPNode> indexPair2 in dpTable[jp1 + k][im1 - k])
                        {
                            long key = compute_rule_key(indexPair1.Key, indexPair2.Key);
                            if (!NTtoNT.ContainsKey(key)) continue;
                            
                            DPNode content = new DPNode(indexPair1.Key, indexPair2.Key, indexPair1.Value, indexPair2.Value);
                            Ks[j].set(i);
                            foreach (long ruleIndex in NTtoNT[key])
                            {
                                Di[ruleIndex] = content;
                                if (START_RULE == ruleIndex) startNode = content; 
                            }
                        }
                    }
                }
            }
        }
        
        if (startNode != null)
        {
            wordInGrammar = true;
            parseTree = new TreeNode(START_RULE, NTtoRule.ContainsKey(START_RULE));
            fillTree(parseTree, startNode);
        }
    }
    """