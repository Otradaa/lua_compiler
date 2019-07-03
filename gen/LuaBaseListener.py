# Generated from C:/Users/Julia/Desktop/coursework\Lua.g4 by ANTLR 4.7.2
import sys
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LuaParser import LuaParser
else:
    from LuaParser import LuaParser

# This class defines a complete listener for a parse tree produced by LuaParser.
class LuaBaseListener(ParseTreeListener):
    def __init__(self, output, file):
        self.output = output
        self.index = -1
        self.dict = {}
        self.functions = list()
        self.op_comp = {'==':'!=','!=':'==','>':'<=','<':'>=','<=':'>','>=':'<'}
        self.file = file

    # Enter a parse tree produced by LuaParser#chunk.
    def enterChunk(self, ctx:LuaParser.ChunkContext):
        self.output += '\n\n.sub main\n\n'

    # Exit a parse tree produced by LuaParser#chunk.
    def exitChunk(self, ctx:LuaParser.ChunkContext):
        self.output += ctx.getChild(0).block_str
        self.output += '\n.end\n'
        for f in self.functions:
            self.output += f + '\n'
        self.file.write(self.output)

    # Enter a parse tree produced by LuaParser#block.
    def enterBlock(self, ctx:LuaParser.BlockContext):
        pass

    # Exit a parse tree produced by LuaParser#block.
    def exitBlock(self, ctx:LuaParser.BlockContext):
        ctx.block_str = ''
        for child in ctx.children:
            ctx.block_str += child.stat_str


    # Enter a parse tree produced by LuaParser#stat.
    def enterStat(self, ctx:LuaParser.StatContext):
        pass

    # Exit a parse tree produced by LuaParser#stat.
    def exitStat(self, ctx:LuaParser.StatContext):
        ctx.stat_str = ''
        if ctx.getChild(0).getText() == 'while':
            self.index += 1
            ctx.while_label = 'while_loop_{0}'.format(self.index)
            ctx.end_while_label = 'end_while_loop_{0}'.format(self.index)
            ctx.stat_str += '\nwhile_loop_{0}:\n'.format(self.index)
            if isinstance(ctx.getChild(1), LuaParser.ExpContext):
                ctx.stat_str += 'if '+ctx.getChild(1).exp_str + ' goto '+ctx.end_while_label+'\n'
                if isinstance(ctx.getChild(3),LuaParser.BlockContext):
                    ctx.stat_str += ctx.getChild(3).block_str
                    if ctx.getChild(4).getText()=='end':
                        ctx.stat_str += '\ngoto ' + ctx.while_label + '\n'
                        ctx.stat_str += ctx.end_while_label + ':\n'
                        pass
        elif ctx.getChild(0).getText() == 'function':
            self.functions.append(f'.sub {ctx.getChild(1).getChild(0).getText()}\n{ctx.getChild(2).funcbody_str}\n.end\n')
        elif isinstance(ctx.getChild(0),LuaParser.FunctioncallContext):
            ctx.stat_str = ctx.getChild(0).functioncall_str
        elif ctx.getChild(0).getText() == 'if':
            self.index += 1
            ctx.if_label = 'end_if_{0}'.format(self.index)
            ctx.stat_str += '\nif '+ctx.getChild(1).exp_str + ' goto '+ ctx.if_label
            ctx.stat_str += '\n'+ctx.getChild(3).block_str
            ctx.stat_str += '\n' + ctx.if_label + ':\n'
        elif ctx.getChild(0).getText() == 'for':
            self.index += 1
            ind = self.index
            ctx.stat_str += '\nloop_init_{0}:\n'.format(ind)
            ctx.for_counter = ctx.getChild(1).getText()
            ctx.stat_str += '.local pmc {0}\n'.format(ctx.for_counter)
            ctx.stat_str += '{0} = box {1}\n'.format(ctx.for_counter,ctx.getChild(3).exp_str)
            ctx.stat_str += f'\nloop_test_{ind}:\n'
            ctx.stat_str += f'if {ctx.for_counter} < {ctx.getChild(5).getChild(0).exp_str} goto '
            ctx.stat_str += f'loop_body_{ind}\ngoto loop_end_{ind}\n'
            ctx.stat_str += f'\nloop_body_{ind}:\n'
            ctx.stat_str += ctx.getChild(9).block_str
            ctx.stat_str += f'\n\ninc {ctx.for_counter}\ngoto loop_test_{ind}'
            ctx.stat_str += f'\nloop_end_{ind}:\n'

        elif ctx.getChildCount() == 1:
            if isinstance( ctx.getChild(0),LuaParser.FunctioncallContext):
                ctx.stat_str += f'\nsay {ctx.getChild(0).getChild(1).nameandargs_str}\n'
                pass

        else:
            for child in ctx.children:
                if isinstance( child, LuaParser.VarlistContext ):
                    ctx.stat_str += '\n'+child.varlist_str
                elif child.getText() == '=':
                    ctx.stat_str += ' = '
                elif isinstance(child, LuaParser.ExplistContext):
                    #########################
                    if ctx.getChild(0).isnew:
                        ctx.stat_str += f'new "ResizablePMCArray"\n{child.explist_str}' if child.type=='table' else 'new "Integer"'+ \
                            f'{ctx.getChild(0).varlist_str} = {child.explist_str}'
                    else:
                        ctx.stat_str += child.explist_str


                        # Enter a parse tree produced by LuaParser#retstat.
    def enterRetstat(self, ctx:LuaParser.RetstatContext):
        pass

    # Exit a parse tree produced by LuaParser#retstat.
    def exitRetstat(self, ctx:LuaParser.RetstatContext):
        pass


    # Enter a parse tree produced by LuaParser#label.
    def enterLabel(self, ctx:LuaParser.LabelContext):
        pass

    # Exit a parse tree produced by LuaParser#label.
    def exitLabel(self, ctx:LuaParser.LabelContext):
        pass


    # Enter a parse tree produced by LuaParser#funcname.
    def enterFuncname(self, ctx:LuaParser.FuncnameContext):
        pass

    # Exit a parse tree produced by LuaParser#funcname.
    def exitFuncname(self, ctx:LuaParser.FuncnameContext):
        pass


    # Enter a parse tree produced by LuaParser#varlist.
    def enterVarlist(self, ctx:LuaParser.VarlistContext):
        pass

    # Exit a parse tree produced by LuaParser#varlist.
    def exitVarlist(self, ctx:LuaParser.VarlistContext):
        text = ctx.getChild(0).getText()
        if self.dict.keys().__contains__(text):
            ctx.varlist_str = self.dict[text]
            ctx.isnew = False
        elif ctx.getChild(0).getChildCount() == 1:
            self.index += 1
            self.dict[text] = '$P' + str(self.index)
            ctx.varlist_str = f'\n$P{self.index}'
            ctx.isnew = True

        elif isinstance( ctx.getChild(0), LuaParser.VarContext):
            ctx.varlist_str = ctx.getChild(0).var_str
            ctx.isnew = False


    # Enter a parse tree produced by LuaParser#namelist.
    def enterNamelist(self, ctx:LuaParser.NamelistContext):
        pass

    # Exit a parse tree produced by LuaParser#namelist.
    def exitNamelist(self, ctx:LuaParser.NamelistContext):
        pass


    # Enter a parse tree produced by LuaParser#explist.
    def enterExplist(self, ctx:LuaParser.ExplistContext):
        pass

    # Exit a parse tree produced by LuaParser#explist.
    def exitExplist(self, ctx:LuaParser.ExplistContext):
        ctx.explist_str = ''
        if ctx.getChildCount() == 1 and isinstance(ctx.getChild(0), LuaParser.ExpContext):
            ctx.explist_str = ctx.getChild(0).exp_str ######################
            ctx.type = ctx.getChild(0).type ######################
        else:
            for child in ctx.children:
                if child.getText() != ',':
                    ctx.explist_str += child.exp_str
                else:
                    ctx.explist_str += ', '


    # Enter a parse tree produced by LuaParser#exp.
    def enterExp(self, ctx:LuaParser.ExpContext):
        pass

    # Exit a parse tree produced by LuaParser#exp.
    def exitExp(self, ctx:LuaParser.ExpContext):
        ctx.exp_str = ''
        ctx.type = ''
        ctx.need_new=''
        count = ctx.getChildCount()
        if count == 1:
            if ctx.getChild(0).getText() in {'false', 'true'}:
                ctx.exp_str = '1' if ctx.getChild(0).getText() == 'true' else '0'
                ctx.type = 'number'
            elif isinstance(ctx.getChild(0), LuaParser.PrefixexpContext):
                ctx.exp_str = ctx.getChild(0).prefixexp_str
            elif isinstance(ctx.getChild(0), LuaParser.NumberContext):
                ctx.exp_str = ctx.getChild(0).getChild(0).getText()
                ctx.type = 'number'
            elif isinstance(ctx.getChild(0), LuaParser.TableconstructorContext):
                ctx.exp_str = ctx.getChild(0).tableconstructor_str
                ctx.type = 'table'
        elif count == 3:
            if isinstance(ctx.getChild(1), LuaParser.OperatorComparisonContext):
                ctx.exp_str = ctx.getChild(0).exp_str + ' '
                ctx.exp_str += self.op_comp[ctx.getChild(1).op_comparison_str]
                ctx.exp_str += ' ' + ctx.getChild(2).exp_str
            elif isinstance(ctx.getChild(1), LuaParser.OperatorAddSubContext):
                ctx.exp_str = ctx.getChild(0).exp_str + ' '
                ctx.exp_str += ctx.getChild(1).getChild(0).getText()######
                ctx.exp_str += ' ' + ctx.getChild(2).exp_str
                #self.index += 1
                #self.dict[text] = '$P' + str(self.index)
                ##ctx.exp_str = '$P' + str(self.index)
                #ctx.need_new = '$P' + str(self.index)+' = '+ctx.getChild(0).exp_str + ' '+ctx.getChild(1).getText()+\
                #    ' ' + ctx.getChild(0).exp_str

    # Enter a parse tree produced by LuaParser#prefixexp.
    def enterPrefixexp(self, ctx:LuaParser.PrefixexpContext):
        pass

    # Exit a parse tree produced by LuaParser#prefixexp.
    def exitPrefixexp(self, ctx:LuaParser.PrefixexpContext):
        ctx.prefixexp_str =''
        if ctx.getChildCount() == 1 and isinstance(ctx.getChild(0), LuaParser.VarOrExpContext):
            ctx.prefixexp_str = ctx.getChild(0).varorexp_str
        elif ctx.getChildCount() == 2 and \
            isinstance(ctx.getChild(0),LuaParser.VarOrExpContext) and \
            isinstance(ctx.getChild(1), LuaParser.NameAndArgsContext):
            if ctx.getChild(0).varorexp_str == 'length':
                ctx.prefixexp_str = self.dict[ctx.getChild(1).nameandargs_str].replace('$','')
                pass

    # Enter a parse tree produced by LuaParser#functioncall.
    def enterFunctioncall(self, ctx:LuaParser.FunctioncallContext):
        pass

    # Exit a parse tree produced by LuaParser#functioncall.
    def exitFunctioncall(self, ctx:LuaParser.FunctioncallContext):
        if ctx.getChild(0).varorexp_str == 'print':
            ctx.functioncall_str = f'\nsay {ctx.getChild(1).nameandargs_str}\n'
        else:
            ctx.functioncall_str = f'\n{ctx.getChild(0).varorexp_str}({ctx.getChild(1).nameandargs_str})\n'



    # Enter a parse tree produced by LuaParser#varOrExp.
    def enterVarOrExp(self, ctx:LuaParser.VarOrExpContext):
        pass

    # Exit a parse tree produced by LuaParser#varOrExp.
    def exitVarOrExp(self, ctx:LuaParser.VarOrExpContext):
        if isinstance(ctx.getChild(0), LuaParser.VarContext):
            ctx.varorexp_str = ctx.getChild(0).var_str

    # Enter a parse tree produced by LuaParser#var.
    def enterVar(self, ctx:LuaParser.VarContext):
        pass

    # Exit a parse tree produced by LuaParser#var.
    def exitVar(self, ctx:LuaParser.VarContext):
        ctx.var_str = ''
        if ctx.getChildCount() == 2:
            if ctx.getChild(0).getText() == 'table' and ctx.getChild(1).getText() == 'varSuffix':
                ctx.var_str = 'length' ############ it's a len
            elif self.dict.keys().__contains__(ctx.getChild(0).getText())and isinstance(ctx.getChild(1),LuaParser.VarSuffixContext):
                ctx.var_str = self.dict[ctx.getChild(0).getText()] + ctx.getChild(1).varsuffix_str
        elif self.dict.keys().__contains__(ctx.getText()):
            ctx.var_str = self.dict[ctx.getText()]
        else:
            ctx.var_str = ctx.getText()

            # Enter a parse tree produced by LuaParser#varSuffix.
    def enterVarSuffix(self, ctx:LuaParser.VarSuffixContext):
        pass

    # Exit a parse tree produced by LuaParser#varSuffix.
    def exitVarSuffix(self, ctx:LuaParser.VarSuffixContext):
        ctx.varsuffix_str = ''
        if ctx.getChildCount() ==3:
            ctx.varsuffix_str = '['+ctx.getChild(1).exp_str+']'


    # Enter a parse tree produced by LuaParser#nameAndArgs.
    def enterNameAndArgs(self, ctx:LuaParser.NameAndArgsContext):
        pass

    # Exit a parse tree produced by LuaParser#nameAndArgs.
    def exitNameAndArgs(self, ctx:LuaParser.NameAndArgsContext):
        if ctx.getChildCount() == 1 \
                and isinstance(ctx.getChild(0), LuaParser.ArgsContext):
            ctx.nameandargs_str = ctx.getChild(0).args_str

    # Enter a parse tree produced by LuaParser#args.
    def enterArgs(self, ctx:LuaParser.ArgsContext):
        pass

    # Exit a parse tree produced by LuaParser#args.
    def exitArgs(self, ctx:LuaParser.ArgsContext):
        ctx.args_str = ''
        if ctx.getChildCount() > 1 \
                and isinstance(ctx.getChild(1), LuaParser.ExplistContext):
            ctx.args_str = ctx.getChild(1).explist_str

    # Enter a parse tree produced by LuaParser#functiondef.
    def enterFunctiondef(self, ctx:LuaParser.FunctiondefContext):
        pass

    # Exit a parse tree produced by LuaParser#functiondef.
    def exitFunctiondef(self, ctx:LuaParser.FunctiondefContext):
        pass


    # Enter a parse tree produced by LuaParser#funcbody.
    def enterFuncbody(self, ctx:LuaParser.FuncbodyContext):
        namelist = ctx.getChild(1).getChild(0)
        if isinstance(namelist, LuaParser.NamelistContext):
            for child in namelist.children:
                if child.getText() != ',':
                    self.dict[child.getText()] = child.getText()

    # Exit a parse tree produced by LuaParser#funcbody.
    def exitFuncbody(self, ctx:LuaParser.FuncbodyContext):
        ctx.funcbody_str = ''
        namelist = ctx.getChild(1).getChild(0)
        if isinstance(namelist, LuaParser.NamelistContext):
            for child in namelist.children:
                if child.getText() != ',':
                    ctx.funcbody_str += f'.param pmc {child.getText()}\n'
            ctx.funcbody_str += ctx.getChild(3).block_str
        else:
            ctx.funcbody_str += ctx.getChild(2).block_str


    # Enter a parse tree produced by LuaParser#parlist.
    def enterParlist(self, ctx:LuaParser.ParlistContext):
        pass

    # Exit a parse tree produced by LuaParser#parlist.
    def exitParlist(self, ctx:LuaParser.ParlistContext):
        pass


    # Enter a parse tree produced by LuaParser#tableconstructor.
    def enterTableconstructor(self, ctx:LuaParser.TableconstructorContext):
        pass

    # Exit a parse tree produced by LuaParser#tableconstructor.
    def exitTableconstructor(self, ctx:LuaParser.TableconstructorContext):
        ctx.tableconstructor_str = ''
        if isinstance(ctx.getChild(1), LuaParser.FieldlistContext):
            ctx.tableconstructor_str = ctx.getChild(1).fieldlist_str


    # Enter a parse tree produced by LuaParser#fieldlist.
    def enterFieldlist(self, ctx:LuaParser.FieldlistContext):
        pass

    # Exit a parse tree produced by LuaParser#fieldlist.
    def exitFieldlist(self, ctx:LuaParser.FieldlistContext):
        fieldlist_str = ''
        i = 1
        for child in ctx.children:
            if isinstance(child, LuaParser.FieldContext):
                fieldlist_str += '$P' + str(self.index) + '[' + str(i) + '] = ' + str(
                    child.getChild(0).getChild(0).getText()) + '\n'
                i += 1
        ctx.fieldlist_str = fieldlist_str

    # Enter a parse tree produced by LuaParser#field.
    def enterField(self, ctx:LuaParser.FieldContext):
        pass

    # Exit a parse tree produced by LuaParser#field.
    def exitField(self, ctx:LuaParser.FieldContext):
        pass


    # Enter a parse tree produced by LuaParser#fieldsep.
    def enterFieldsep(self, ctx:LuaParser.FieldsepContext):
        pass

    # Exit a parse tree produced by LuaParser#fieldsep.
    def exitFieldsep(self, ctx:LuaParser.FieldsepContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorOr.
    def enterOperatorOr(self, ctx:LuaParser.OperatorOrContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorOr.
    def exitOperatorOr(self, ctx:LuaParser.OperatorOrContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorAnd.
    def enterOperatorAnd(self, ctx:LuaParser.OperatorAndContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorAnd.
    def exitOperatorAnd(self, ctx:LuaParser.OperatorAndContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorComparison.
    def enterOperatorComparison(self, ctx:LuaParser.OperatorComparisonContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorComparison.
    def exitOperatorComparison(self, ctx:LuaParser.OperatorComparisonContext):
        ctx.op_comparison_str = ctx.getText()

    # Enter a parse tree produced by LuaParser#operatorStrcat.
    def enterOperatorStrcat(self, ctx:LuaParser.OperatorStrcatContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorStrcat.
    def exitOperatorStrcat(self, ctx:LuaParser.OperatorStrcatContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorAddSub.
    def enterOperatorAddSub(self, ctx:LuaParser.OperatorAddSubContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorAddSub.
    def exitOperatorAddSub(self, ctx:LuaParser.OperatorAddSubContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorMulDivMod.
    def enterOperatorMulDivMod(self, ctx:LuaParser.OperatorMulDivModContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorMulDivMod.
    def exitOperatorMulDivMod(self, ctx:LuaParser.OperatorMulDivModContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorBitwise.
    def enterOperatorBitwise(self, ctx:LuaParser.OperatorBitwiseContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorBitwise.
    def exitOperatorBitwise(self, ctx:LuaParser.OperatorBitwiseContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorUnary.
    def enterOperatorUnary(self, ctx:LuaParser.OperatorUnaryContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorUnary.
    def exitOperatorUnary(self, ctx:LuaParser.OperatorUnaryContext):
        pass


    # Enter a parse tree produced by LuaParser#operatorPower.
    def enterOperatorPower(self, ctx:LuaParser.OperatorPowerContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorPower.
    def exitOperatorPower(self, ctx:LuaParser.OperatorPowerContext):
        pass


    # Enter a parse tree produced by LuaParser#number.
    def enterNumber(self, ctx:LuaParser.NumberContext):
        pass

    # Exit a parse tree produced by LuaParser#number.
    def exitNumber(self, ctx:LuaParser.NumberContext):
        pass


    # Enter a parse tree produced by LuaParser#string.
    def enterString(self, ctx:LuaParser.StringContext):
        pass

    # Exit a parse tree produced by LuaParser#string.
    def exitString(self, ctx:LuaParser.StringContext):
        pass


