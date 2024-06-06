from useraccount.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['name','email','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password doesnot match')
     
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']


class UserChangePasswordSerializer(serializers.Serializer):
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)

    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        
        if check_password(password,user.password):
            raise serializers.ValidationError('New password must be different from the current password.')

        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password doesnot match')


        
        user.set_password(password)

        user.save()
        
        
        return attrs


class SendPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self,attrs):
        email = attrs.get('email')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded uid',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password reset token',token)
            
            #Provide your site link to replace it 
            
            link = 'http://localhost:3000/reset-password/' + uid + '/' + token
            print('Password reset link',link)


            #send email 
            body = 'Click the following link to reset your password' + ' ' +link
            data = {
                "subject":"Reset Your Password",
                "body":body,
                "to_email":user.email

            }
            Util.send_email(data)
            return attrs
            

        else:
            raise serializers.ValidationError('You are not registered user')
        

class UserPasswordResetSerializer(serializers.Serializer):
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)

    
    def validate(self,attrs):
        try:

            password = attrs.get('password')
            password2 = attrs.get('password2')

            uid = self.context.get('uid')
            token = self.context.get('token')

            id = smart_str(urlsafe_base64_decode(uid))     #smart_str converts to strings
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not valid or expired.')
            
            if check_password(password,user.password):
                raise serializers.ValidationError('New password must be different from the current password.')

            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password doesnot match')


            
            user.set_password(password)

            user.save()
            
            
            return attrs
        except DjangoUnicodeDecodeError as idetifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or expired.')
        
        # we used try ..except for further security to prevent unauthorized person from manipulating the uid 